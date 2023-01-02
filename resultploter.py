import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import  MultipleLocator
from matmodplot import savefig_nomargin
import numpy as np
import os


# function which can read inp file
def inp_reader(file_path):
    with open(file_path, 'r') as file:
            data = file.readlines()
    return data

def subfolder_name_reader(output_dir):
    subfolders=[]
    for (root,dirs,files) in os.walk(output_dir): 
        subfolders.append(dirs)
    subfolders=subfolders[0]
    return subfolders

def resultfig(axins_dim=[0.07, 0.77, 0.15, 0.15]):
    ax_fontsize , axin_fontsize = 8, 6.5
    plt.rcParams.update({'font.size': ax_fontsize})
    fig1, ax1 = plt.subplots(figsize=(6, 4.5))
    fig1.subplots_adjust(right=0.8)
    ax1.set_xlabel(xlabel='Displacement load (mm)', labelpad=0)
    ax1.set_ylabel(ylabel='Solid line: Max Hoop stress (Mpa)', labelpad=0)
    ax1_1=ax1.twinx()
    ax1_2=ax1.twinx()
    ax1_1.set_xlabel(xlabel='Displacement load (mm)', labelpad=0)
    ax1_1.set_ylabel(ylabel='Dotted line: Concrete Reaction (KN)', labelpad=0)
    ax1_2.set_xlabel(xlabel='Displacement load (mm)', labelpad=0)
    ax1_2.set_ylabel(ylabel='Dashed line: Yarn Reaction at loaded end (KN)', labelpad=0)
    ax1_2.spines.right.set_position(("axes", 1.1))
    plt.rcParams.update({'font.size': axin_fontsize})
    axins = ax1.inset_axes(axins_dim)
    axins.set_xlabel(xlabel='Displacement load \n (mm)', labelpad=0)
    axins.set_ylabel(ylabel='Yarn stress (Gpa)' , labelpad=0 )
    axins.xaxis.set_major_locator(MultipleLocator(0.2))
    axins.yaxis.set_major_locator(MultipleLocator(1))
    secax_x = axins.secondary_xaxis('top')
    secax_y = axins.secondary_yaxis('right')
    plt.rcParams.update({'font.size': ax_fontsize})
    return ax1, ax1_1, ax1_2, axins, secax_x, secax_y
    
def resultploter(ax1, ax1_1, ax1_2, axins, path):
    
    simulation_name=os.path.basename(os.path.normpath(path))
    # assign path of monitor.csv 
    Monitor_dir_path = os.path.join(path, "AtenaCalculation/monitors.csv")
    # assign path of inp file (.inp )
    Inp_dir_path = os.path.join(path, "AtenaCalculation/{}.inp".format(simulation_name))  

    # all data included in .inp file are stored in the variable inp_data 
    inp_data=inp_reader(Inp_dir_path)

    # extracting total number of nodes and corresponding coordinates
    for line in inp_data:
        if line.find('Coordinate definition. Suma=') != -1:
            number_of_nodes=int(inp_data[inp_data.index(line)].split("=",1)[1].strip())
            node_coords = pd.DataFrame(inp_data[inp_data.index(line)+2:inp_data.index(line)+number_of_nodes+2])
            node_coords=node_coords[0].str.split(expand = True)

    # defining columns for panda dataframe based on monitors.csv / constructing monitors dataframe which includes all data of monitors.csv
    names=np.arange(0,100) # make it better to avoid unused space
    monitors = pd.read_csv(Monitor_dir_path, sep=';', names=names, skiprows=0)           ### start here
    # extracting lines in which stresses of interface nodes are stored from that line (for all steps)
    lines_interface_stresses=monitors.index[monitors[1].str.contains('MONITOR_SET_2_INTERFACE-STRESSES', case=True, na=False)].values

    # extracting lines in which diss of interface nodes are stored from that line (for all steps)
    lines_interface_diss=monitors.index[monitors[1].str.contains('MONITOR_SET_2_INTERFACE-DISS', case=True, na=False)].values

    # extracting interface node ID and coordinates
    interface_nodes_id=pd.DataFrame(monitors[1].values[lines_interface_stresses[0:len(lines_interface_stresses)]])
    interface_nodes_id=pd.to_numeric(interface_nodes_id[0].str.split(pat="_", expand = True)[4])
    interface_nodes_coords=np.array(node_coords.iloc[interface_nodes_id-1])
    y_coord=np.array(interface_nodes_coords[:, 2],dtype=np.float_)
    x_coord=np.array(interface_nodes_coords[:, 1],dtype=np.float_)
    interface_nodes_id=np.array(interface_nodes_coords[:, 0],dtype=np.int_) #Defined again to be sure that the order of data remains unchanged

    # extracting total number of steps 
    steps=int(monitors[2].values[lines_interface_stresses[0]+2].strip())
    steps_array=np.arange(0,steps+1)

    # constructing a 2D array containing interface nodes data including node ID, Y-coordinates, stress, and relative displacement in the tangential and normal direction
    nodes_data = np.zeros((len(lines_interface_stresses), 2 + 4*steps))
    nodes_data[:, 0] = interface_nodes_id
    nodes_data[:, 1] = y_coord
    for i in range(len(lines_interface_stresses)):
        Sigma_tt = np.array(monitors[3].values[lines_interface_stresses[i]+7:lines_interface_stresses[i]+7+steps], dtype=np.float_)
        Sigma_nn = np.array(monitors[4].values[lines_interface_stresses[i]+7:lines_interface_stresses[i]+7+steps], dtype=np.float_)
        dV = np.array(monitors[3].values[lines_interface_diss[i]+7:lines_interface_diss[i]+7+steps], dtype=np.float_)
        dU = np.array(monitors[4].values[lines_interface_diss[i]+7:lines_interface_diss[i]+7+steps], dtype=np.float_)
        nodes_data[i, 2:2+steps] = Sigma_tt
        nodes_data[i, 2+steps:2+2*steps] = Sigma_nn
        nodes_data[i, 2+2*steps:2+3*steps] = dV
        nodes_data[i, 2+3*steps:] = dU

    critical_load_step=np.argmax(nodes_data[-1, 2:2+steps])+1   # it indicates the load step in which a point in the interface starts to be
                                                                # damaged if loaded more than it  in our case, the point of the interface where
                                                                # damage initiation occurred on it first, is the nearest point on the interface to the loaded end
                                                            
                                                                
    # steps considered for plotting. acceptable rang from 1 to steps
    step_to_plot_p1=np.around(np.linspace(1, critical_load_step, num=4)).astype(int)
    step_to_plot_p2=np.around(np.linspace(critical_load_step+1, steps, num=4)).astype(int)
    step_to_plot=np.append(step_to_plot_p1,step_to_plot_p2)
    step_to_plot.sort()


    # defines :label for  critical load step, decohesion initiation load step and last load step
    #         :dashed linestyle for steps before critical load step and solid for the rest
    def label_linewidth(step_to_plot):
        if step_to_plot==critical_load_step: label='Step {}: critical load step'.format(s)
        elif  step_to_plot==critical_load_step+1: label='Step {}: decohesion initiation load step'.format(s)
        elif  step_to_plot==steps: label='Step {}: last load step'.format(s)
        else: label='Step {}'.format(s)
        if step_to_plot <= critical_load_step: linestyle='dashed'
        else: linestyle='solid'
        return label, linestyle
    
    # extracting load displacement 
    if monitors.index[monitors[1].str.contains('AV_DISS_TOP', case=True, na=False)].size==0:
        print("there is no monitor defined for AV_DISS_TOP of yarn")
    else:
        line=int(monitors.index[monitors[1].str.contains('AV_DISS_TOP', case=True, na=False)].values)
        unit=''.join(monitors[3].values[line+5]).strip()
        Diss_load=monitors[3].values[line+6:line+6+steps+1].astype(float)

    # plotting Max Hoop stress evolution in concrete (Mpa)
    if monitors.index[monitors[3].str.contains('sigma_tt', case=True, na=False)].size==0:
        print("there is no monitor defined for max hoop stress in concrete")
    else:
        line_maxhoop=int(monitors.index[monitors[3].str.contains('sigma_tt', case=True, na=False)].values)
        unit=''.join(monitors[3].values[line_maxhoop+1]).strip()
        if ''.join(monitors[3].values[line_maxhoop+2]).strip() == "NaN":
                sigma_tt=monitors[3].values[line_maxhoop+3:line_maxhoop+3+steps].astype(float)
                sigma_tt=np.insert(sigma_tt, 0, 0)
        else:
                sigma_tt=monitors[3].values[line_maxhoop+2:line_maxhoop+3+steps].astype(float)

    ax1.plot(Diss_load*1000, sigma_tt , linewidth=1) 
    # xmax = Diss_load[np.argmax(sigma_tt)]*1000
    # ymax = sigma_tt.max()
    # ax1.plot((xmax, xmax), (0, ymax), linewidth=0.4 , linestyle='dashed' , color='k')


    # plotting pullout curve and CON_REACTION
    if monitors.index[monitors[1].str.contains('CON_REACTION', case=True, na=False)].size==0:
        print("there is no monitor defined for reaction of concrete's fixed end")
    else:
        line=int(monitors.index[monitors[1].str.contains('CON_REACTION', case=True, na=False)].values)
        unit=''.join(monitors[3].values[line+5]).strip()
        if ''.join(monitors[3].values[line+6]).strip() == "NaN":
                C_R=monitors[3].values[line+7:line+7+steps].astype(float)
                C_R=np.insert(C_R, 0, 0)
        else:
                C_R=monitors[3].values[line+6:line+6+steps].astype(float)
    ax1_1.plot(Diss_load*1000, -C_R*1000, linestyle='dotted', linewidth=1)
    # xmax = Diss_load[np.argmax(-C_R)]*1000
    # ymax = (-C_R*1000).max()
    # ax1_1.plot((xmax, xmax), (0, ymax), linewidth=0.4 , linestyle='dashed' , color='r')


    if monitors.index[monitors[1].str.contains('SUM-REACTION_TOP', case=True, na=False)].size==0:
        print("there is no monitor defined for yarn at the fixed end")
    else:
        line=int(monitors.index[monitors[1].str.contains('SUM-REACTION_TOP', case=True, na=False)].values)
        unit=''.join(monitors[3].values[line+5]).strip()
        if ''.join(monitors[3].values[line+6]).strip() == "NaN":
                Yarn_R_T=monitors[3].values[line+7:line+7+steps].astype(float)
                Yarn_R_T=np.insert(Yarn_R_T, 0, 0)
        else:
                Yarn_R_T=monitors[3].values[line+6:line+6+steps].astype(float)
    ax1_2.plot(Diss_load*1000, Yarn_R_T*1000, linestyle='dashed', linewidth=1)
    

    # plotting YARN_TENSILE_STRESS
    if monitors.index[monitors[1].str.contains('YARN_TENSILE_STRESS', case=True, na=False)].size==0:
        print("there is no monitor defined for reaction of concrete's fixed end")
    else:
        line=int(monitors.index[monitors[1].str.contains('YARN_TENSILE_STRESS', case=True, na=False)].values)
        unit=''.join(monitors[3].values[line+5]).strip()
        if ''.join(monitors[3].values[line+6]).strip() == "NaN":
                Yarn_M_S=monitors[3].values[line+7:line+7+steps].astype(float)
                Yarn_M_S=np.insert(Yarn_M_S, 0, 0)
        else:
                Yarn_M_S=monitors[3].values[line+6:line+6+steps].astype(float)
    axins.plot(Diss_load*1000, Yarn_M_S/1000,  linewidth=0.7 )
    #acceptable_step=next(x[0] for x in enumerate(Yarn_M_S) if x[1] > 3300)-1
    xmax = Diss_load[np.argmax(Yarn_M_S)]*1000
    ymax = (Yarn_M_S/1000).max()
    return xmax, ymax

output_dir = "C:/Users/adelpasand/Desktop/Dec-paramstudy"
paramstudies = subfolder_name_reader(output_dir)  
for PS in paramstudies:
    ax1, ax1_1, ax1_2, axins, secax_x, secax_y= resultfig()
    ps_path = os.path.join(output_dir, PS)
    Simulations_name = subfolder_name_reader(ps_path)
    X_extraticks, Y_extraticks=[], []
    for sn in Simulations_name:
        path = os.path.join(ps_path, sn)
        xmax, ymax = resultploter(ax1, ax1_1, ax1_2, axins, path)
        X_extraticks.append(xmax)
        Y_extraticks.append(ymax)
    X_extraticks = list(set(X_extraticks)) # Repeated items should be deleted
    Y_extraticks = list(set(Y_extraticks)) 
    Y_extraticks = [max(Y_extraticks)]
    secax_x.set_xticks(X_extraticks)
    secax_y.set_yticks(Y_extraticks)
    savefig_nomargin(ps_path, 'results of {}'.format(PS))
print('figs saved in {}'.format(output_dir))
#plt.show()
