import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os
from material_model_ploter import 


# function which can read inp file
def inp_reader(file_path):
    with open(file_path, 'r') as file:
            data = file.readlines()
    return data




plt.rcParams.update({'font.size': 8})


for study in [1]:
    
    fig1, axs1 = plt.subplots(figsize=(7.5, 4.5))
    fig1.subplots_adjust(right=0.8)
    axs1_1=axs1.twinx()
    axs1_2=axs1.twinx()
    axins = axs1.inset_axes([0.1, 0.5, 0.47, 0.4])
    axins.plot([7,8,9],[2,8,6])

    fig2, axs2 = plt.subplots()
    fig2.suptitle('Max Tensile Stress In Yarn')
    
    for index in [1,2,3]:
        
        # assign path of monitor.csv 
        Monitor_dir_path = "C:/Users/adelpasand/Desktop/PS{}/axi-Diss controlled with softening in Ktt- 1mm 150 step C {} .gid/AtenaCalculation/monitors.csv".format(study, index)  
        # assign path of inp file (.inp )
        Inp_dir_path = "C:/Users/adelpasand/Desktop/PS{}/axi-Diss controlled with softening in Ktt- 1mm 150 step C {} .gid/AtenaCalculation/axi-Diss controlled with softening in Ktt- 1mm 150 step try2.inp".format(study, index)   

        # all data included in .inp file are stored in the variable inp_data 
        inp_data=inp_reader(Inp_dir_path)

        # extracting total number of nodes and corresponding coordinates
        for line in inp_data:
            if line.find('Coordinate definition. Suma=') != -1:
                number_of_nodes=int(inp_data[inp_data.index(line)].split("=",1)[1].strip())
                node_coords = pd.DataFrame(inp_data[inp_data.index(line)+2:inp_data.index(line)+number_of_nodes+2])
                node_coords=node_coords[0].str.split(expand = True)

        # defining columns for panda dataframe based on monitors.csv / costructing monitors dataframe which includes all data of monitors.csv
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

        axs1.set(xlabel='Displacement load (mm)', ylabel='Solid line: Max Hoop stress (Mpa)')
        axs1.plot(Diss_load*1000, sigma_tt , label='C={} MPa'.format(index), linewidth=1) 
        """ xmax = steps_array[np.argmax(sigma_tt)]
        ymax = sigma_tt.max() """
        # axs.plot((xmax, xmax), (0, ymax), linewidth=0.4 , linestyle='dashed' , color='k')
        """ extraticks=[steps]
        new_xticks=list(plt.xticks()[0]) + extraticks
        new_xticks.remove(160)
        plt.xticks(new_xticks) """
        """ X_extraticks=[xmax]
        Y_extraticks=[ymax]
        secax_x = axs1.secondary_xaxis('top')
        secax_x.set_xticks(X_extraticks)
        secax_y = axs1.secondary_yaxis('right')
        secax_y.set_yticks(Y_extraticks) """


        # plotting pullout curve
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
        axs1_1.set(xlabel='Displacement load (mm)', ylabel='Dotted line: Concrete Reaction (KN)')
        axs1_1.plot(Diss_load*1000, -C_R*1000, linestyle='dotted', linewidth=1)
        """ xmax = steps_array[np.argmax(-Yarn_M_S)]
        ymax = (-Yarn_M_S*1000000).max() """
        # axs.plot((xmax, xmax), (0, ymax), linewidth=0.4 , linestyle='dashed' , color='k')
        """ extraticks=[steps]
        new_xticks=list(plt.xticks()[0]) + extraticks
        new_xticks.remove(160)
        new_xticks.remove(-20)
        plt.xticks(new_xticks) """
        """ X_extraticks=[xmax]
        Y_extraticks=[ymax]
        secax_x = axs2.secondary_xaxis('top')
        secax_x.set_xticks(X_extraticks)
        secax_y = axs2.secondary_yaxis('right')
        secax_y.set_yticks(Y_extraticks) """

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
        axs1_2.set(xlabel='Displacement load (mm)', ylabel='Dashed line: Yarn Reaction at loaded end (KN)')
        axs1_2.plot(Diss_load*1000, Yarn_R_T*1000, linestyle='dashed', linewidth=1)
        axs1_2.spines.right.set_position(("axes", 1.12))




        """ xmax = steps_array[np.argmax(-Yarn_M_S)]
        ymax = (-Yarn_M_S*1000000).max() """
        # axs.plot((xmax, xmax), (0, ymax), linewidth=0.4 , linestyle='dashed' , color='k')
        """ extraticks=[steps]
        new_xticks=list(plt.xticks()[0]) + extraticks
        new_xticks.remove(160)
        new_xticks.remove(-20)
        plt.xticks(new_xticks) """
        """ X_extraticks=[xmax]
        Y_extraticks=[ymax]
        secax_x = axs2.secondary_xaxis('top')
        secax_x.set_xticks(X_extraticks)
        secax_y = axs2.secondary_yaxis('right')
        secax_y.set_yticks(Y_extraticks) """




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

        axs2.set(xlabel='Displacement load (mm)', ylabel='Stress (MPa)')
        axs2.plot(Diss_load*1000, Yarn_M_S , label='C={} MPa'.format(index))
        #acceptable_step=next(x[0] for x in enumerate(Yarn_M_S) if x[1] > 3300)-1
        xmax = steps_array[np.argmax(Yarn_M_S)]
        ymax = (Yarn_M_S).max()
        # axs.plot((xmax, xmax), (0, ymax), linewidth=0.4 , linestyle='dashed' , color='k')
        """ extraticks=[steps]
        new_xticks=list(plt.xticks()[0]) + extraticks
        new_xticks.remove(160)
        new_xticks.remove(-20)
        plt.xticks(new_xticks) """
        X_extraticks=[xmax]
        Y_extraticks=[ymax]
        secax_x = axs2.secondary_xaxis('top')
        secax_x.set_xticks(X_extraticks)
        secax_y = axs2.secondary_yaxis('right')
        secax_y.set_yticks(Y_extraticks)
axs1.legend()
axs2.legend()
plt.show()




