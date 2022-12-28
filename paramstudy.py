import numpy as np
from inpgenrun import *
from matmodplot import *

def PS1():
    ratio=2
    C_0= np.array([1,2,3])
    ft_0=np.array([C_0[0],C_0[0],C_0[0]])
    Ktt=5000
    phi=0.3#
    Knn=5000
    N_ratio=2
    fig1, ax1, axins1, axins2 = figs()
    current_inp_path = r"C:\Users\adelpasand\Desktop\axi-dec\axi-Diss controlled with softening in Ktt- 0.7mm 150 step.gid\AtenaCalculation\axi-Diss controlled with softening in Ktt- 0.7mm 150 step.inp"
    output_dir = "C:/Users/adelpasand/Desktop/axi-dec/PS1"
   
    Du_f, Ft_Du_f = N_TSL_ploter(axins2, ft_0[0], Knn, N_ratio)
    for i, value in enumerate(C_0):
        c , ft = C_0[i], ft_0[i]
        Dv_f, C_Dv_f = bilin_TSL_ploter(fig1, ax1, c, Ktt, ratio, hatch='false', legend='off')
        interface_parameters_changer(current_inp_path, output_dir, str(i+1), Knn,Ktt,c,phi,ft, soft_hard_fun = [Du_f, Ft_Du_f, Dv_f, C_Dv_f])
        threshold_ploter(fig1, axins1, c, ft, phi, max(C_0))
    path_ploter(axins1, ft_0, C_0)
    savefig_nomargin(output_dir,'PS1')


def PS2():
    ratio=2
    C_0= 1 
    c=C_0
    ft=C_0
    phi=0.3
    Ktt=[5000,5000/2,5000/3]
    Knn=5000
    N_ratio=2
    fig1, ax1, axins1, axins2  = figs(axins_dim1=[0.8, 0.79, 0.18, 0.18],axins_dim2=[0.8, 0.52, 0.18, 0.18])
    current_inp_path = r"C:\Users\adelpasand\Desktop\axi-dec\axi-Diss controlled with softening in Ktt- 0.7mm 150 step.gid\AtenaCalculation\axi-Diss controlled with softening in Ktt- 0.7mm 150 step.inp"
    output_dir = "C:/Users/adelpasand/Desktop/axi-dec/PS2"
    Du_f, Ft_Du_f = N_TSL_ploter(axins2, ft, Knn, N_ratio)
    for i, value in enumerate(Ktt):
        Dv_f, C_Dv_f = bilin_TSL_ploter(fig1, ax1, c, value, ratio, hatch='false', legend='off')
        threshold_ploter(fig1, axins1, c, ft, phi, c)
        interface_parameters_changer(current_inp_path, output_dir, str(i+1), Knn,value,c,phi,ft, soft_hard_fun = [Du_f, Ft_Du_f, Dv_f, C_Dv_f])
    savefig_nomargin(output_dir,'PS2')

    

def PS3():
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
    N_ratio=2
    fig1, ax1, axins1, axins2  = figs()
    current_inp_path = r"C:\Users\adelpasand\Desktop\axi-dec\axi-Diss controlled with softening in Ktt- 0.7mm 150 step.gid\AtenaCalculation\axi-Diss controlled with softening in Ktt- 0.7mm 150 step.inp"
    output_dir = "C:/Users/adelpasand/Desktop/axi-dec/PS3"
    Du_f, Ft_Du_f = N_TSL_ploter(axins2, ft_0[0], Knn, N_ratio)
    for i, value in enumerate(r):
        c, ktt,ft = C_0[i], Ktt[i], ft_0[i]
        Dv_f, C_Dv_f = bilin_TSL_ploter(fig1, ax1, c, ktt, ratio, hatch='false', legend='off')
        threshold_ploter(fig1, axins1, c, ft, phi, max(C_0))
        interface_parameters_changer(current_inp_path, output_dir, str(i+1), Knn,ktt,c,phi,ft, soft_hard_fun = [Du_f, Ft_Du_f, Dv_f, C_Dv_f])
    path_ploter(axins1, ft_0, C_0)
    savefig_nomargin(output_dir, 'PS3')


    
def PS4():
    ratio=[1, 1.5 ,2, 3]
    C_0 = 2 
    ft=C_0
    ktt=5000
    H = 2000
    phi=0.3
    Knn=5000
    N_ratio=2
    fig1, ax1, axins1, axins2  = figs()
    current_inp_path = r"C:\Users\adelpasand\Desktop\axi-dec\axi-Diss controlled with softening in Ktt- 0.7mm 150 step.gid\AtenaCalculation\axi-Diss controlled with softening in Ktt- 0.7mm 150 step.inp"
    output_dir = "C:/Users/adelpasand/Desktop/axi-dec/PS4"
    Du_f, Ft_Du_f = N_TSL_ploter(axins2, ft, Knn, N_ratio)
    for i, value in enumerate(ratio):
            Dv_f, C_Dv_f = bilin_TSL_ploter(fig1, ax1, C_0, ktt, value)
            if i==0:
                interface_parameters_changer(current_inp_path, output_dir, str(i+1), Knn,ktt,C_0,phi,ft)
            else:
                interface_parameters_changer(current_inp_path, output_dir, str(i+1), Knn,ktt,C_0,phi,ft, soft_hard_fun = [Du_f, Ft_Du_f, Dv_f, C_Dv_f])
    Dv_f, C_Dv_f = plateau_TSL_ploter(fig1, ax1, C_0, ktt, 2*ratio[-1]-1)
    interface_parameters_changer(current_inp_path, output_dir, '5', Knn,ktt,C_0,phi,ft, soft_hard_fun = [Du_f, Ft_Du_f, Dv_f, C_Dv_f])
    Dv_f, C_Dv_f = hardening_TSL_ploter(fig1, ax1, C_0, ktt, H, H/ktt*(ratio[-1]-1)**2+(2*ratio[-1]-1), hatch='false', legend='off')
    interface_parameters_changer(current_inp_path, output_dir, '6', Knn, ktt, C_0, phi, ft, soft_hard_fun = [Du_f, Ft_Du_f, Dv_f, C_Dv_f])
    threshold_ploter(fig1, axins1, C_0, ft, phi,C_0)
    savefig_nomargin(output_dir,'PS4')
 

PS4() 
