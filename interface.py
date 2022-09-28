import numpy as np
import os
import subprocess
import time
import progressbar

def inp_reader(file_path):
    with open(file_path, 'r') as file:
            data = file.readlines()
    return data


def Material_search():
    Material_db = []
    count_m=0
    for line in data:
        if line.find('MATERIAL ID') != -1:
            count_m += 1
            Material_db.extend([data.index(line)+1, line.strip(), data[data.index(line)+1].strip(), data[data.index(line)+2].strip()])
    print('\n', '{} material model exist in the inp file as below:'.format(count_m), '\n')
    for i in range(count_m):
        print(Material_db[4*(i)+1], '\n', Material_db[4*(i)+2], '\n', Material_db[4*(i)+3], '\n',
        'located in Line Number {}'.format(Material_db[4*(i)]), '\n')
    return Material_db
    

def interface_parameters_changer(K_NN_MIN, K_NN_MAX,
                             K_NN_N, K_TT_MIN, K_TT_MAX, K_TT_N,
                             COHESION_MIN, COHESION_MAX, COHESION_N,
                             FRICTION_MIN, FRICTION_MAX, FRICTION_N,
                             FT_MIN, FT_MAX, FT_N,
                             eitc):
    new_models_list = []
    all_models_name = []
    all_models_name.append(file_path.split('\\')[-1][:-4])
    if 'TYPE "CC2DInterface"' in Material_db:
        count = Material_db.count('TYPE "CC2DInterface"')
        if count > 1:
            print ('There is more than one material model for the TYPE TYPE "CC2DInterface", which one do you want to consider for parametric study?')
            indexs = [i for i, x in enumerate(Material_db) if x == 'TYPE "CC2DInterface"']
            for i in indexs:
                print('{} with name {}'.format(Material_db[i-2], Material_db[i-1]))
            ID=input('Enter the coresponding material ID:   ')       
            line = Material_db[Material_db.index('MATERIAL ID {}'.format(ID))-1]
        else:
            line = Material_db[Material_db.index('TYPE "CC2DInterface"')-3]       
        K_NN_range=np.linspace(K_NN_MIN, K_NN_MAX, num=K_NN_N)
        nknn=np.shape(K_NN_range)[0] #Number of K_NN quantities in the range
        K_TT_range=np.linspace(K_TT_MIN, K_TT_MAX, num=K_TT_N)
        nktt=np.shape(K_TT_range)[0] #Number of K_NN quantities in the range
        COHESION_range=np.linspace(COHESION_MIN, COHESION_MAX, num=COHESION_N)
        nc=np.shape(COHESION_range)[0] #Number of COHESION quantities in the range
        FRICTION_range=np.linspace(FRICTION_MIN, FRICTION_MAX, num=FRICTION_N)
        nf=np.shape(FRICTION_range)[0] #Number of FRICTION quantities in the range
        FT_range=np.linspace(FT_MIN, FT_MAX, num=FT_N)
        nft=np.shape(FT_range)[0] #Number of FT quantities in the range
        neitc=np.size(eitc)  #Number of tension conditions
        for count1, values in enumerate(K_NN_range,start=1):
            data[line+2]= '  K_NN     {:.6e}\n'.format(values)
            data[line+7]= '  K_NN_MIN     {:.6e}\n'.format(values/1000)
            for count2, values in enumerate(K_TT_range,start=1):  
                data[line+3]= '  K_TT     {:.6e}\n'.format(values)
                data[line+8]= '  K_TT_MIN     {:.6e}\n'.format(values/1000)
                for count3, values in enumerate(COHESION_range,start=1):  
                    data[line+4]= '  COHESION     {:.6e}\n'.format(values)
                    for count4, values in enumerate(FRICTION_range,start=1): 
                        data[line+5]= '  FRICTION     {:.6e}\n'.format(values)
                        for count5, values in enumerate(FT_range,start=1): 
                            data[line+6]= '  FT     {:.6e}\n'.format(values)
                            for count6, values in enumerate(eitc,start=1): 
                                data[line+9]= '  TENSION_ELIPS {}\n'.format(values)
                                overall_counter=(count1-1)*nktt*nc*nf*nft*neitc+(count2-1)*nc*nf*nft*neitc+(count3-1)*nf*nft*neitc+(count4-1)*nft*neitc+(count5-1)*neitc+count6
                                name = "{}_Model_{}_{}_{}_{}_{}_{}".format(overall_counter, count1,count2,count3,count4,count5,count6)
                                new_models_list.append(name)
                                all_models_name.append(name)
                                for x in data:
                                    if x.find(all_models_name[overall_counter-1]) != -1:
                                        data[data.index(x)]=data[data.index(x)].replace(all_models_name[overall_counter-1], name)
                                bat_dir = os.path.join(output_dir, name)
                                calculation_path = os.path.join(bat_dir, "AtenaCalculation")
                                os.makedirs(calculation_path)
                                inp_path = os.path.join(calculation_path, name+".inp")  
                                with open(inp_path, 'w') as f:
                                    f.writelines(data)
                                bat_path = os.path.join(bat_dir, name+".bat") 
                                #bat_file_content='cd AtenaCalculation\n\ncmd /K start /B "ATENA calculation" %AtenaConsole64% /M CCStructures /execute /catch_fp_instructs /o "{}.inp" "{}.out" "{}.msg" "{}.err" /num_unused_threads=2  /num_iters_per_thread=0'.format(name,name,name,name)
                                bat_file_content='cd AtenaCalculation\n\ncmd /C start /B "ATENA calculation" %AtenaConsole64% /M CCStructures /execute /catch_fp_instructs /o "{}.inp" "{}.out" "{}.msg" "{}.err" /num_unused_threads=2  /num_iters_per_thread=0'.format(name,name,name,name)
                                with open(bat_path, 'w') as f:
                                    f.writelines(bat_file_content) 
                                    print("output directory, inp file and bat file of the model '% s' created" % name)
        print('\n', '--------------> {} models created in total <--------------'.format(overall_counter))
        print('\n')
    else:
        print('No CC2DInterface material found in the inp file')
    return new_models_list
        

def yarn_parameters_changer(E_MIN, E_MAX, E_N, MU_MIN, MU_MAX, MU_N, RHO_MIN, RHO_MAX, RHO_N, ALPHA_MIN, ALPHA_MAX, ALPHA_N):
    new_models_list = []
    all_models_name = []
    all_models_name.append(file_path.split('\\')[-1][:-4])
    if 'TYPE "CC3DElastIsotropic"' in Material_db:
        count = Material_db.count('TYPE "CC3DElastIsotropic"')
        if count > 1:
            print ('There is more than one material model for the TYPE "CC3DElastIsotropic", which one do you want to consider for parametric study?')
            indexs = [i for i, x in enumerate(Material_db) if x == 'TYPE "CC3DElastIsotropic"']
            for i in indexs:
                print('{} with name {}'.format(Material_db[i-2], Material_db[i-1]))
            ID=input('Enter the coresponding material ID:   ')       
            line = Material_db[Material_db.index('MATERIAL ID {}'.format(ID))-1]
        else:
            line = Material_db[Material_db.index('TYPE "CC3DElastIsotropic"')-3]
        E_range=np.linspace(E_MIN, E_MAX, num=E_N)
        ne=np.shape(E_range)[0] #Number of E quantities in the range
        MU_range=np.linspace(MU_MIN, MU_MAX, num=MU_N)
        nmu=np.shape(MU_range)[0] #Number of K_NN quantities in the range
        RHO_range=np.linspace(RHO_MIN, RHO_MAX, num=RHO_N)
        nrho=np.shape(RHO_range)[0] #Number of COHESION quantities in the range
        ALPHA_range=np.linspace(ALPHA_MIN, ALPHA_MAX, num=ALPHA_N)
        nalpha=np.shape(ALPHA_range)[0] #Number of FRICTION quantities in the range
        for count1, values in enumerate(E_range,start=1):
            data[line+2]= '  E     {:.6e}\n'.format(values)
            for count2, values in enumerate(MU_range,start=1):  
                data[line+3]= '  MU     {:.6e}\n'.format(values)
                for count3, values in enumerate(RHO_range,start=1):  
                    data[line+4]= '  RHO     {:.6e}\n'.format(values)
                    for count4, values in enumerate(ALPHA_range,start=1): 
                        data[line+5]= '  ALPHA     {:.6e}\n'.format(values)
                        overall_counter=(count1-1)*nmu*nrho*nalpha+(count2-1)*nmu*nrho+(count3-1)*nmu+count4
                        name = "{}_Model_{}_{}_{}_{}".format(overall_counter, count1,count2,count3,count4)
                        new_models_list.append(name)
                        all_models_name.append(name)
                        for x in data:
                            if x.find(all_models_name[overall_counter-1]) != -1:
                                data[data.index(x)]=data[data.index(x)].replace(all_models_name[overall_counter-1], name)
                        bat_dir = os.path.join(output_dir, name)
                        calculation_path = os.path.join(bat_dir, "AtenaCalculation")
                        os.makedirs(calculation_path)
                        inp_path = os.path.join(calculation_path, name+".inp")  
                        with open(inp_path, 'w') as f:
                            f.writelines(data)
                        bat_path = os.path.join(bat_dir, name+".bat") 
                        #bat_file_content='cd AtenaCalculation\n\ncmd /K start /B "ATENA calculation" %AtenaConsole64% /M CCStructures /execute /catch_fp_instructs /o "{}.inp" "{}.out" "{}.msg" "{}.err" /num_unused_threads=2  /num_iters_per_thread=0'.format(name,name,name,name)
                        bat_file_content='cd AtenaCalculation\n\ncmd /C start /B "ATENA calculation" %AtenaConsole64% /M CCStructures /execute /catch_fp_instructs /o "{}.inp" "{}.out" "{}.msg" "{}.err" /num_unused_threads=2  /num_iters_per_thread=0'.format(name,name,name,name)
                        with open(bat_path, 'w') as f:
                            f.writelines(bat_file_content) 
                            print("output directory, inp file and bat file of the model '% s' created" % name)
        print('\n', '--------------> {} models created in total <--------------'.format(overall_counter))
        print('\n')
    else:
        print('No CC3DElastIsotropic material found in the inp file')
    return new_models_list



def run_inps(model):
    print('Simulation is running for %s' %model)
    bat_dir = os.path.join(output_dir, model)   
    os.chdir(bat_dir)
    bat_path = os.path.join(bat_dir, model+".bat") 
    bar = progressbar.ProgressBar(max_value=progressbar.UnknownLength)
    p = subprocess.Popen([bat_path], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
    while p.stdout is not None:
        bar.update()
        line = p.stdout.readline()
        if not line:            
            print('--------> Simulation Completed <--------','\n')
            p.stdout.flush()
            break
        
      
def countdown(input_time): 
    # countdown function. input should be in second. use it in the for loop over the run_inps() function to be sure that
    # all output files saved before going to the next simulation
    while input_time:
        mins, secs = divmod(input_time, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print('running the next simulation in ', timer, end="\r")
        time.sleep(1)
        input_time -= 1
 

file_path = r"C:\Users\adelpasand\Desktop\axi\3D axi bond slip law (jump and slip) with monitoring.inp"
output_dir = "C:/Users/adelpasand/Desktop/parametric_study"   
data=inp_reader(file_path)
Material_db = Material_search()




K_NN_MIN=5000; K_NN_MAX=10000; K_NN_N=1 # _MIN , _MAX , _N define the Min, Max and number of quantities in range including Min and Max
K_TT_MIN=5000; K_TT_MAX=12000; K_TT_N=5
COHESION_MIN=2; COHESION_MAX=6; COHESION_N=5
FRICTION_MIN=0.3; FRICTION_MAX=0.45; FRICTION_N=3
FT_MIN=1.5; FT_MAX=3; FT_N=1  #checking the validity of dependency between parameters--> dependency conditions: FT<C and FT<C/FRICTION
eitc = [-1,1] # elips in tension conditions: [-1] means de-activating and [1] means activating
                # the ellipsoidal shape of criterion in tension, i.e. for tensile normal stress shape
                # in case of [-1,1], both condition will be considered
new_models_list = interface_parameters_changer(K_NN_MIN, K_NN_MAX,
                             K_NN_N, K_TT_MIN, K_TT_MAX, K_TT_N,
                             COHESION_MIN, COHESION_MAX, COHESION_N,
                             FRICTION_MIN, FRICTION_MAX, FRICTION_N,
                             FT_MIN, FT_MAX, FT_N,
                             eitc)


E_MIN=25000; E_MAX=30000; E_N=3
MU_MIN= 0.25; MU_MAX= 0.35; MU_N=1
RHO_MIN=0; RHO_MAX=0; RHO_N=1
ALPHA_MIN=0; ALPHA_MAX=0; ALPHA_N=1
""" new_models_list = yarn_parameters_changer(E_MIN, E_MAX, E_N,
                        MU_MIN, MU_MAX, MU_N,
                        RHO_MIN, RHO_MAX, RHO_N,
                        ALPHA_MIN, ALPHA_MAX, ALPHA_N) """



for model in new_models_list:
    run_inps(model)
    countdown(10)



    