import numpy as np
from inpgenrun import *
from matmodplot import *
from psresultplot import * 

def PS1(name, current_inp_path):
    ratio=2
    C_0= np.array([1,2,3])
    ft_0=np.array([C_0[0],C_0[0],C_0[0]])
    Ktt=5000
    phi=0.3#
    Knn=5000
    N_ratio=6
    fig1, ax1, axins1, axins2 = figs()
    PS_dir = os.path.join(output_dir, name)
    Du_f, Ft_Du_f = N_TSL_ploter(axins2, ft_0[0], Knn, N_ratio)
    print('parametric study {}: plotting(.pdf) interface material models for parametric study and Generating corresponding inp and bat file'. format(name))
    for i, value in enumerate(C_0):
        c , ft = C_0[i], ft_0[i]
        Dv_f, C_Dv_f = bilin_TSL_ploter(fig1, ax1, c, Ktt, ratio, hatch='false', legend='off')
        interface_parameters_changer(current_inp_path, PS_dir, str(i+1), Knn,Ktt,c,phi,ft, Ft_soft_hard_fun=[Du_f, Ft_Du_f], C_soft_hard_fun=[Dv_f, C_Dv_f])
        threshold_ploter(fig1, axins1, c, ft, phi, max(C_0))
    path_ploter(axins1, ft_0, C_0)
    savefig_nomargin(PS_dir, name)

def PS2(name, current_inp_path):
    ratio=2
    C_0= 1 
    c=C_0
    ft=C_0
    phi=0.3
    Ktt=[5000,5000/2,5000/3]
    Knn=5000
    N_ratio=6
    fig1, ax1, axins1, axins2  = figs(axins_dim1=[0.8, 0.79, 0.18, 0.18],axins_dim2=[0.8, 0.52, 0.18, 0.18])
    PS_dir = os.path.join(output_dir, name)
    Du_f, Ft_Du_f = N_TSL_ploter(axins2, ft, Knn, N_ratio)
    print('parametric study {}: plotting(.pdf) interface material models for parametric study and Generating corresponding inp and bat file'. format(name))
    for i, value in enumerate(Ktt):
        Dv_f, C_Dv_f = bilin_TSL_ploter(fig1, ax1, c, value, ratio, hatch='false', legend='off')
        threshold_ploter(fig1, axins1, c, ft, phi, c)
        interface_parameters_changer(current_inp_path, PS_dir, str(i+1), Knn,value,c,phi,ft, Ft_soft_hard_fun=[Du_f, Ft_Du_f], C_soft_hard_fun=[Dv_f, C_Dv_f])
    savefig_nomargin(PS_dir, name)

def PS3(name, current_inp_path):
    ratio=2
    phi=0.3
    C_0_min= 1 
    C_0_Max= 3
    Ktt=5000
    r=np.linspace(1,C_0_Max/C_0_min,3)
    C_0=r*C_0_min
    ft_0=np.array([C_0[0],C_0[0],C_0[0]])
    Ktt=r*Ktt
    Knn=5000
    N_ratio=6
    fig1, ax1, axins1, axins2  = figs()
    PS_dir = os.path.join(output_dir, name)
    Du_f, Ft_Du_f = N_TSL_ploter(axins2, ft_0[0], Knn, N_ratio)
    print('parametric study {}: plotting(.pdf) interface material models for parametric study and Generating corresponding inp and bat file'. format(name))
    for i, value in enumerate(r):
        c, ktt,ft = C_0[i], Ktt[i], ft_0[i]
        Dv_f, C_Dv_f = bilin_TSL_ploter(fig1, ax1, c, ktt, ratio, hatch='false', legend='off')
        threshold_ploter(fig1, axins1, c, ft, phi, max(C_0))
        interface_parameters_changer(current_inp_path, PS_dir, str(i+1), Knn,ktt,c,phi,ft, Ft_soft_hard_fun=[Du_f, Ft_Du_f], C_soft_hard_fun=[Dv_f, C_Dv_f])
    path_ploter(axins1, ft_0, C_0)
    savefig_nomargin(PS_dir, name)

def PS4(name, current_inp_path):
    ratio=[1, 1.5 ,2, 3]
    C_0 = 1 
    ft=1
    ktt=5000
    H = 2000
    phi=0.3
    Knn=5000
    N_ratio=6
    fig1, ax1, axins1, axins2  = figs()
    PS_dir = os.path.join(output_dir, name)
    Du_f, Ft_Du_f = N_TSL_ploter(axins2, ft, Knn, N_ratio)
    print('parametric study {}: plotting(.pdf) interface material models for parametric study and Generating corresponding inp and bat file'. format(name))
    for i, value in enumerate(ratio):
            Dv_f, C_Dv_f = bilin_TSL_ploter(fig1, ax1, C_0, ktt, value)
            if i==0:
                interface_parameters_changer(current_inp_path, PS_dir, str(i+1), Knn,ktt,C_0,phi,ft, Ft_soft_hard_fun=[Du_f, Ft_Du_f])
            else:
                interface_parameters_changer(current_inp_path, PS_dir, str(i+1), Knn,ktt,C_0,phi,ft, Ft_soft_hard_fun=[Du_f, Ft_Du_f], C_soft_hard_fun=[Dv_f, C_Dv_f])
    Dv_f, C_Dv_f = plateau_TSL_ploter(fig1, ax1, C_0, ktt, 2*ratio[-1]-1)
    interface_parameters_changer(current_inp_path, PS_dir, '5', Knn,ktt,C_0,phi,ft, Ft_soft_hard_fun=[Du_f, Ft_Du_f], C_soft_hard_fun=[Dv_f, C_Dv_f])
    Dv_f, C_Dv_f = hardening_TSL_ploter(fig1, ax1, C_0, ktt, H, H/ktt*(ratio[-1]-1)**2+(2*ratio[-1]-1), hatch='false', legend='off')
    interface_parameters_changer(current_inp_path, PS_dir, '6', Knn, ktt, C_0, phi, ft, Ft_soft_hard_fun=[Du_f, Ft_Du_f], C_soft_hard_fun=[Dv_f, C_Dv_f])
    threshold_ploter(fig1, axins1, C_0, ft, phi,C_0)
    savefig_nomargin(PS_dir, name)

def PS5(name, current_inp_path):
    phi=0.3
    C_0= 1 
    c=C_0
    Ktt_0=5000
    ration0=2
    Dv_f=ration0*C_0/Ktt_0
    r=[1,4/3,ration0,4]
    ft_0=1
    ft=ft_0
    Knn=5000
    N_ratio=6
    fig1, ax1, axins1, axins2  = figs()
    PS_dir = os.path.join(output_dir, name)
    Du_f, Ft_Du_f = N_TSL_ploter(axins2, ft_0, Knn, N_ratio)
    print('parametric study {}: plotting(.pdf) interface material models for parametric study and Generating corresponding inp and bat file'. format(name))
    for i, value in enumerate(r):
        ktt=value*Ktt_0/ration0
        Dv_f, C_Dv_f = bilin_TSL_ploter(fig1, ax1, c, ktt, value, hatch='false', legend='off')
        threshold_ploter(fig1, axins1, c, ft, phi, c)
        if value==1:
            interface_parameters_changer(current_inp_path, PS_dir, str(i+1), Knn,ktt,C_0,phi,ft, Ft_soft_hard_fun=[Du_f, Ft_Du_f])
        else:
            interface_parameters_changer(current_inp_path, PS_dir, str(i+1), Knn,ktt,c,phi,ft, Ft_soft_hard_fun=[Du_f, Ft_Du_f], C_soft_hard_fun=[Dv_f, C_Dv_f])
    #path_ploter(axins1, ft_0, C_0)
    savefig_nomargin(PS_dir, name)

def Vast_PS(name, current_inp_path):
    index=0
    ft_0=1
    Knn=5000
    N_ratio=6
    phi=0.3
    C_0= [1,2,3]
    DV_e= np.around(np.arange(0.0001,0.0013,0.0001),6)
    ax_fontsize  = 12
    plt.rcParams.update({'font.size': ax_fontsize})
    fig1, ax1 = plt.subplots()
    ax1.set(xlabel='Dv (sliding (mm)) ', ylabel='Shear Stress (MPa)')
    DU, sigma = N_TSL(ft_0, Knn, N_ratio)
    Du_f, Ft_Du_f =  DU[-1], sigma[-1]
    PS_dir = os.path.join(output_dir, name)
    for i , C_0_value in enumerate(C_0):
        for j , DV_e_value in enumerate(DV_e):
            ktt=C_0[i]/DV_e[j]
            Dv_f=DV_e[j:]
            for k, Dv_f_value in enumerate(Dv_f):
                index+=1
                ratio=ktt*Dv_f_value/C_0[i]
                Dv_f, C_Dv_f = bilin_TSL_ploter(fig1, ax1, C_0[i], ktt, ratio , hatch='false', legend='off', linewidth=0.5)  
                #threshold_ploter(fig1, axins1, C_0[i], ft_0, phi, max(C_0))
                if ratio==1:
                    interface_parameters_changer(current_inp_path, PS_dir, str(index), Knn,ktt,C_0[i],phi,ft_0, Ft_soft_hard_fun=[Du_f, Ft_Du_f])
                else:
                    interface_parameters_changer(current_inp_path, PS_dir, str(index), Knn,ktt,C_0[i],phi,ft_0, Ft_soft_hard_fun=[Du_f, Ft_Du_f], C_soft_hard_fun=[Dv_f_value, C_Dv_f])
    print('parametric study {}: plotting(.pdf) interface material models for parametric study and Generating corresponding inp and bat file'. format(name))
    savefig_nomargin(PS_dir, name)    
    
def Verify_PS(name, current_inp_path):
    index=0
    material_mu =np.array([[1.5, 0.00062, 0.00085],
                [1.5, 0.00062, 0.00093],
                [2.5, 0.00062, 0.00085],
                [2.5, 0.00062, 0.00093],
                [2.75, 0.00105 ,0.00113]])
    fig1, ax1 = plt.subplots()
    ax_fontsize  = 12
    plt.rcParams.update({'font.size': ax_fontsize})
    ax1.set(xlabel='Dv (sliding (mm)) ', ylabel='Shear Stress (MPa)')
    for m , value in enumerate (material_mu[0:5]):
        index += 1
        C_0=material_mu[m,0]
        DV_e=material_mu[m,1]
        Dv_f=material_mu[m,2]
        ft_0=1
        Knn=5000
        N_ratio=6
        phi=0.3
        DU, sigma = N_TSL(ft_0, Knn, N_ratio)
        Du_f, Ft_Du_f =  DU[-1], sigma[-1]
        PS_dir = os.path.join(output_dir, name)
        ktt=C_0/DV_e
        ratio=ktt*Dv_f/C_0
        Dv_f, C_Dv_f = bilin_TSL_ploter(fig1, ax1, C_0, ktt, ratio , hatch='false', legend='off', linewidth=0.5)  
        #threshold_ploter(fig1, axins1, C_0[i], ft_0, phi, max(C_0))
        if ratio==1:
            interface_parameters_changer(current_inp_path, PS_dir, str(index), Knn,ktt,C_0,phi,ft_0, Ft_soft_hard_fun=[Du_f, Ft_Du_f])
        else:
            interface_parameters_changer(current_inp_path, PS_dir, str(index), Knn,ktt,C_0,phi,ft_0, Ft_soft_hard_fun=[Du_f, Ft_Du_f], C_soft_hard_fun=[Dv_f, C_Dv_f])
    print('parametric study {}: plotting(.pdf) interface material models for parametric study and Generating corresponding inp and bat file'. format(name))
    savefig_nomargin(PS_dir, name)
    
def runallmodels(output_dir):
    paramstudies = subfolder_name_reader(output_dir)  
    for PS in paramstudies:
        ps_path = os.path.join(output_dir, PS)
        Simulations_name = subfolder_name_reader(ps_path)
        Simulations_name=list(map(int, Simulations_name))
        Simulations_name=sorted(Simulations_name)
        Simulations_name=Simulations_name[208:]
        Simulations_name=list(map(str, Simulations_name))
        for sn in Simulations_name:
            path = os.path.join(ps_path, sn)
            print(path)
            run_inps(path, sn)
            for i in range(1,151):
                path_to_del = os.path.join(path, "AtenaCalculation/{}.{:04}".format(sn,i))
                os.remove(path_to_del)
            countdown(10)


output_dir = "C:/Users/adelpasand/Desktop/new-jan-PS/"
current_inp_path = r"C:\Users\adelpasand\Desktop\axi-dec\axi-Diss controlled with softening in Ktt- 0.7mm 150 step.gid\AtenaCalculation\axi-Diss controlled with softening in Ktt- 0.7mm 150 step.inp"

# PS1('PS1', current_inp_path) 
# PS2('PS2', current_inp_path) 
# PS3('PS3', current_inp_path) 
# PS4('PS4', current_inp_path) 
# PS5('PS5', current_inp_path) 

#Vast_PS('Vast_PS', current_inp_path)

#Verify_PS('Verify_PS', current_inp_path)

#runallmodels(output_dir)

# psresultploter(output_dir)
runoverall_simresultploter_part1(output_dir)

