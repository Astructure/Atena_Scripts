import numpy as np
import os
import subprocess
import time
import progressbar

def inp_reader(file_path):
    with open(file_path, 'r') as file:
            data = file.readlines()
    return data

def inp_miner():
    data=inp_reader(file_path)
    Material_db = []
    Function_block_info=[]
    count_m=0
    temp_counter=0
    for line in data:
        if line.find('MATERIAL ID') != -1:
            count_m += 1
            while True:
                temp_counter += 1
                end_index=data.index(line)+temp_counter
                if data[end_index].find(';') != -1:
                    temp_counter=0
                    break
            start_index=data.index(line)
            start_line=start_index+1
            Material_db.extend([start_line, line.strip(), data[start_index+1].strip(), data[start_index+2].strip(), end_index ])
        if line.find('FUNCTION ID 10001') != -1:
            start_index=data.index(line)
            while True:
                temp_counter += 1
                end_index=start_index+temp_counter
                if data[end_index].find(';') != -1:
                    break
            Function_block_info.extend([start_index, end_index])
        if line.find('TASK name') != -1:
            old_inp_task_name=line.strip('TASK name')[1:-2] #usage of [1:-2] is to aviod picking " ".
    print('\n', '{} material model exist in the inp file as below:'.format(count_m), '\n')
    for i in range(count_m):
        print(Material_db[5*(i)+1], '\n', Material_db[5*(i)+2], '\n', Material_db[5*(i)+3], '\n',
        'located in Line Number {}'.format(Material_db[5*(i)]), '\n')
    return data, Material_db, Function_block_info, old_inp_task_name

def interface_parameters_changer(new_inp_name, K_NN ,K_TT,C_0,phi,FT_0,eitc=1,rdc={}, soft_hard_fun=[]):
    # eitc: defines elips in tension conditions: -1 means de-activating and 1 means activating
    #                 # the ellipsoidal shape of criterion in tension, i.e. for tensile normal stress shape
    # rdc:  defines the moving gap (reset displacement).
    #       admissible value for rdc is -1 (top surface/line for all coresponding elements will be realigned at the end of each step)
    #       or 1 (bottom surface/line for coresponding elementswill be realigned at the end of each step)
    # soft_hard_fun = [Du_f, Ft_Du_f, Dv_f, C_Dv_f]
    data, Material_db, Function_block_info, old_inp_task_name  = inp_miner()
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
        del data[Material_db[0]+2:Material_db[4]]
        data.insert(line+2, '  K_NN     {:.6e}\n'.format(K_NN))
        data.insert(line+3, '  K_TT     {:.6e}\n'.format(K_TT))
        data.insert(line+4, '  COHESION     {:.6e}\n'.format(C_0))   
        data.insert(line+5, '  FRICTION     {:.6e}\n'.format(phi))
        data.insert(line+6, '  FT     {:.6e}\n'.format(FT_0))
        data.insert(line+7, '  K_NN_MIN     {:.6e}\n'.format(K_NN/1000))
        data.insert(line+8, '  K_TT_MIN     {:.6e}\n'.format(K_TT/1000))
        if not soft_hard_fun:
            data.insert(line+9, '  TENSION_ELIPS {}\n'.format(eitc))
            if rdc:
                data.insert(line+10, '  RESET_DISPLS {}\n'.format(rdc))
        else:
            data.insert(line+9, '  TENSION_SOFT_HARD_FUNCTION 10001\n')
            data.insert(line+10, '  COHESION_SOFT_HARD_FUNCTION 10002\n')
            data.insert(line+11, '  TENSION_ELIPS {}\n'.format(eitc))
            if rdc:
                data.insert(line+12, '  RESET_DISPLS {}\n'.format(rdc))
            data.insert(Function_block_info[0], '  FUNCTION ID 10001\n')
            data.insert(Function_block_info[0], '  NAME "TENSION_SOFT_HARD_FUNCTION Function for CC2DInterface material"\n')
            data.insert(Function_block_info[0], '  TYPE "CCMultiLinearFunction" REMOVE_ALL\n')
            data.insert(Function_block_info[0], '  xvalues     0.0     {}\n'.format(soft_hard_fun[0]))
            data.insert(Function_block_info[0], '  yvalues     1.0     {}\n'.format(soft_hard_fun[1]))
            data.insert(Function_block_info[0], 'FUNCTION ID 10002\n')
            data.insert(Function_block_info[0], '  NAME "COHESION_SOFT_HARD_FUNCTION Function for CC2DInterface material"\n')
            data.insert(Function_block_info[0], '  TYPE "CCMultiLinearFunction" REMOVE_ALL\n')
            data.insert(Function_block_info[0], '  xvalues     0.0     {}\n'.format(soft_hard_fun[2]))
            data.insert(Function_block_info[0], '  yvalues     1.0     {}\n'.format(soft_hard_fun[3]))
            data.insert(Function_block_info[0], ' ;\n')
        for x in data:
            if x.find(old_inp_task_name) != -1:
                data[data.index(x)]=data[data.index(x)].replace(old_inp_task_name, new_inp_name)
        bat_dir = os.path.join(output_dir, new_inp_name)
        calculation_path = os.path.join(bat_dir, "AtenaCalculation")
        os.makedirs(calculation_path)
        inp_path = os.path.join(calculation_path, new_inp_name+".inp")  
        with open(inp_path, 'w') as f:
            f.writelines(data)
        bat_path = os.path.join(bat_dir, new_inp_name+".bat") 
        #bat_file_content='cd AtenaCalculation\n\ncmd /K start /B "ATENA calculation" %AtenaConsole64% /M CCStructures /execute /catch_fp_instructs /o "{}.inp" "{}.out" "{}.msg" "{}.err" /num_unused_threads=2  /num_iters_per_thread=0'.format(name,name,name,name)
        bat_file_content='cd AtenaCalculation\n\ncmd /C start /B "ATENA calculation" %AtenaConsole64% /M CCStructures /execute /catch_fp_instructs /o "{}.inp" "{}.out" "{}.msg" "{}.err" /num_unused_threads=2  /num_iters_per_thread=0'.format(new_inp_name,new_inp_name,new_inp_name,new_inp_name)
        with open(bat_path, 'w') as f:
            f.writelines(bat_file_content) 
            print("output directory, inp file and bat file of the model '% s' created" % new_inp_name)
    else:
        print('No CC2DInterface material found in the inp file')
            

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
 

file_path = r"C:\Users\adelpasand\Desktop\axi-dec\check\test- 0.7mm 150 step.inp"
output_dir = "C:/Users/adelpasand/Desktop/axi-dec/check_output"   


K_NN=5000
K_TT=5000
COHESION=2
FRICTION=0.3
FT=1.5
new_inp_name='1'
interface_parameters_changer(new_inp_name, K_NN,K_TT,COHESION,FRICTION,FT)




    