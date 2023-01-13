import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from collections import Counter
from matplotlib.ticker import  MultipleLocator
from matmodplot import savefig_nomargin
import numpy as np
import os


# function which can read inp file
def inp_reader(file_path):
    with open(file_path, 'r') as file:
            data = file.readlines()
    return data


# function simresultploter_part1 plots     1: plotting Tangential and Normal Stress profile along the interface
#                                          2: plotting Tangential and Normal Relative Displacements profile along the Interface     
#                                          3: plotting Relative Opening of Interface with respect to fixed end and with respect to loaded end'
#                                          4: plotting Normalized Opening of Interface with respect to fixed end and with respect to loaded end
#                                          5: plotting Normal Relative Displacements of Interface(opening) for all steps. focus is on profile
#                                             evolution and zoom in on the loaded end opening   
#                                          6: plotting Tangential and Normal Relative Displacements Evolution of Interface in selected nodes   
#                                          7: plotting Tangential and Normal stresses Evolution of Interface in selected nodes 
#
def simresultploter_part1(path):   
      
      # path: first level folder of each simulation 
      simulation_name=os.path.basename(os.path.normpath(path))
      Inp_dir_path = os.path.join(path, "AtenaCalculation/{}.inp".format(simulation_name)) 
      Monitor_dir_path = os.path.join(path, "AtenaCalculation/monitors.csv")      
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
      if  critical_load_step == steps:
            critical_load_step=[]
            # steps considered for plotting. acceptable rang from 1 to steps
            print('info: there is no damaged point in whole interface i.e the interface remained totally undamaged')
            step_to_plot=np.around(np.linspace(1, steps, num=8)).astype(int)
            step_to_plot.sort()                                                
      else:
            step_to_plot_p1=np.around(np.linspace(1, critical_load_step, num=4)).astype(int)
            step_to_plot_p2=np.around(np.linspace(critical_load_step+1, steps, num=4)).astype(int)
            step_to_plot=np.append(step_to_plot_p1,step_to_plot_p2)
            step_to_plot.sort()

      # extracting load displacement 
      if monitors.index[monitors[1].str.contains('AV_DISS_TOP', case=True, na=False)].size==0:
        print("there is no monitor defined for AV_DISS_TOP of yarn")
      else:
            line=int(monitors.index[monitors[1].str.contains('AV_DISS_TOP', case=True, na=False)].values)
            unit=''.join(monitors[3].values[line+5]).strip()
            Diss_load=monitors[3].values[line+6:line+6+steps+1].astype(float)
      
      ######################################################################################################
      # plot 1: plotting Tangential and Normal Stress profile along the interface
      plt.rcParams.update({'font.size': 6})
      fig, axs = plt.subplots(2,1, sharex=True)
            #fig.suptitle('Stress profile along the interface')
            #axs[0].set_title('Interface Tangential Stress')
            #axs[1].set_title('Interface Normal Stress ')
      axs[1].set(xlabel='interface length (cm)')
      axs[1].set(ylabel=r'$\sigma$ (MPa)')
      axs[0].set(ylabel=r'$\tau$ (MPa)')
      x_coords = nodes_data[:, 1]
      # defines :label for  critical load step, decohesion initiation load step and last load step
      #         :dashed linestyle for steps before critical load step and solid for the rest
      def label_linewidth(step_to_plot):
            if not critical_load_step:
                  if step_to_plot==steps: label='load {:.3f} mm: last load step'.format(Diss_load[step_to_plot]*1000)
                  else: label='load {:.3f} mm'.format(Diss_load[step_to_plot]*1000)
                  linestyle='dashed'
            else:
                  if step_to_plot==critical_load_step: label='load {:.4f} mm: critical load step'.format(Diss_load[step_to_plot]*1000)
                  elif  step_to_plot==critical_load_step+1: label='load {:.4f} mm: decohesion initiation load step'.format(Diss_load[step_to_plot]*1000)
                  elif  step_to_plot==steps: label='load {:.3f} mm: last load step'.format(Diss_load[step_to_plot]*1000)
                  else: label='load {:.3f} mm'.format(Diss_load[step_to_plot]*1000)
                  if step_to_plot <= critical_load_step: linestyle='dashed'
                  else: linestyle='solid'
            return label, linestyle
      
      for s in step_to_plot:
            Sigma_tt = nodes_data[:, 2 + s-1]
            Sigma_nn = nodes_data[:, 2 + steps + s-1]
            label, linestyle=label_linewidth(s)
            axs[0].plot(x_coords*100, Sigma_tt, label=label, linewidth=0.8, linestyle=linestyle)
            axs[1].plot(x_coords*100, Sigma_nn, label=label, linewidth=0.8, linestyle=linestyle)
      axs[0].legend(prop={'size': 6}, loc='upper left')
      savefig_nomargin(path, '1-Stress profile along the interface')
      plt.close(fig)
      
      ######################################################################################################
      # plot 2: plotting Tangential and Normal Relative Displacements profile along the Interface
      fig, axs = plt.subplots(2,1, sharex=True)
      #fig.suptitle('Relative Displacements profile along the Interface')
      #axs[1].set_title('Normal Relative Displacement (opening)')
      #axs[0].set_title('Tangential Relative Displacements (sliding)')
      axs[1].set(xlabel='Interface Length (cm)', ylabel='Du (mm)')
      axs[0].set(ylabel='Dv (mm)')
      for s in step_to_plot:
            dV = nodes_data[:, 2 + 2*steps +s-1]
            dU = nodes_data[:, 2 + 3*steps + s-1]
            label, linestyle=label_linewidth(s)
            axs[1].plot(x_coords*100, dU*1000, label=label ,linewidth=0.8, linestyle=linestyle)
            axs[0].plot(x_coords*100, dV*1000, label=label ,linewidth=0.8, linestyle=linestyle)
      axs[0].legend(prop={'size': 6}, loc='upper left')
      savefig_nomargin(path, '2-Relative Displacements profile along the Interface')
      plt.close(fig)
      
      ######################################################################################################
      # plot 3: plotting Relative Opening of Interface with respect to fixed end and with respect to loaded end'
      fig, axs = plt.subplots(2,1, sharex=True)
      #fig.suptitle('Relative Opening of Interface')
      #axs[0].set_title('with respect to fixed end')
      #axs[1].set_title('with respect to loaded end')
      axs[1].set(xlabel='Interface Length (cm)', ylabel='Du (mm)')
      axs[0].set(ylabel='Du (mm)') 
      for s in step_to_plot:
            startshifted_dU = nodes_data[:, 2 + 3*steps + s-1]-nodes_data[0, 2 + 3*steps + s-1]
            endshifted_dU = nodes_data[:, 2 + 3*steps + s-1]-nodes_data[-1, 2 + 3*steps + s-1]
            label, linestyle=label_linewidth(s)
            axs[0].plot(x_coords*100, startshifted_dU, label=label , linewidth=0.8 , linestyle=linestyle)
            axs[1].plot(x_coords*100, endshifted_dU, label=label , linewidth=0.8, linestyle=linestyle)
      axs[0].legend(prop={'size': 6}, loc='upper left')
      savefig_nomargin(path, '3-Relative Opening of Interface')
      plt.close(fig)
      
      ######################################################################################################
      # plot 4: plotting Normalized Opening of Interface with respect to fixed end and with respect to loaded end'
      fig, axs = plt.subplots(2,1, sharex=True)
      #fig.suptitle('Normalized Opening of Interface')
      #axs[0].set_title('with respect to fixed end')
      #axs[1].set_title('with respect to loaded end')
      axs[1].set(xlabel='Interface Length (cm)', ylabel='Du_N_fe (-)')
      axs[0].set(ylabel='Du_N_le (-)')
      for s in step_to_plot:
            start_normalized_dU = nodes_data[:, 2 + 3*steps + s-1]/nodes_data[0, 2 + 3*steps + s-1]
            end_normalized_dU = nodes_data[:, 2 + 3*steps + s-1]/nodes_data[-1, 2 + 3*steps + s-1]
            label, linestyle=label_linewidth(s)
            axs[0].plot(x_coords*100, start_normalized_dU, label=label , linewidth=0.8, linestyle=linestyle)
            axs[1].plot(x_coords*100, end_normalized_dU, label=label , linewidth=0.8, linestyle=linestyle)
      axs[0].legend(prop={'size': 6}, loc='upper left')
      savefig_nomargin(path, '4-Normalized Opening of Interface')
      plt.close(fig)
      
      ######################################################################################################
      # plot 5: plotting Normal Relative Displacements of Interface(opening) for all steps. focus is on profile evolution and zoom in on the loaded end opening
      fig, ax = plt.subplots(1,2, figsize=(10,7), gridspec_kw={'width_ratios': [2.5, 1]})
      plt.subplots_adjust(wspace=0.5)
      #fig.suptitle('Normal Relative Displacements of Interface (opening)')
      ax[0].set(xlabel='Interface Length (cm)', ylabel='Du (mm)')
      for s in range(1,steps+1):
            dU = nodes_data[:, 2 + 3*steps + s-1]
            if not critical_load_step:
                  if  s==steps: 
                        label='load {} mm: last load step'.format(Diss_load[s]*1000)
                        linewidth=1.2
                  else: 
                        label=''
                        linewidth=0.4
                  linestyle='dashed'
            else:
                  if s==critical_load_step: 
                        label='load {:.4f} mm: critical load step'.format(Diss_load[s]*1000)
                        linewidth=1.2
                  elif  s==critical_load_step+1: 
                        label='load {:.4f} mm: decohesion initiation load step'.format(Diss_load[s]*1000)
                        linewidth=1.2
                  elif  s==steps: 
                        label='load {} mm: last load step'.format(Diss_load[s]*1000)
                        linewidth=1.2
                  else: 
                        label=''
                        linewidth=0.4
                  if s <= critical_load_step: linestyle='dashed'
                  else: linestyle='solid' 
            ax[0].plot(x_coords*100, dU*1000, label=label, linewidth=linewidth, linestyle=linestyle)
      
      if not critical_load_step:
            critical_load_step=steps
      a=steps-critical_load_step
      b=critical_load_step-1
      if a>=13 and b>=3:
            step_to_plot_p1=np.arange(critical_load_step-3, critical_load_step)
            step_to_plot_p2=np.arange(critical_load_step, critical_load_step+13)
            step_to_plot=np.append(step_to_plot_p1,step_to_plot_p2)
      elif b<3:
            step_to_plot_p1=np.arange(critical_load_step-b, critical_load_step)
            step_to_plot_p2=np.arange(critical_load_step, critical_load_step+13)
            step_to_plot=np.append(step_to_plot_p1,step_to_plot_p2)
      elif a<13:
            step_to_plot_p1=np.arange(critical_load_step-3, critical_load_step)
            step_to_plot_p2=np.arange(critical_load_step, critical_load_step+a+1)
            step_to_plot=np.append(step_to_plot_p1,step_to_plot_p2)
      
      
      h1 = nodes_data[-1, 2 + 3*steps + step_to_plot[-1]-1]*1000
      h0 = nodes_data[490, 2 + 3*steps + step_to_plot[0]-1]*1000
      rect=mpatches.Rectangle((4.9,h0) ,0.1, h1-h0, fill = False, color = "black", linewidth = 0.8)
      ax[0].add_patch(rect)
      ax[0].legend(prop={'size': 6}, loc='upper left')     
      ax[1].set_xlim([4.9, 5.01])
      ax[1].set_ylim([h0, h1])
      for s in step_to_plot:
            dU = nodes_data[:, 2 + 3*steps + s-1]
            label, linewidth=label_linewidth(s)
            ax[1].plot(x_coords*100, dU*1000, label=label ,linewidth=0.8, linestyle=linestyle)          
      ax[1].legend(prop={'size': 6}, loc='lower right')       
      savefig_nomargin(path, '5-Normal Relative Displacements of Interface (opening)')
      plt.close(fig)

      ######################################################################################################
      # plot 6: plotting Tangential and Normal Relative Displacements Evolution of Interface selected nodes   
      fig, ax = plt.subplots(2,1, sharex=True)
      #fig.suptitle('Relative Displacements Evolution in a point of Interface')
      ax[0].set(ylabel='Dv (mm)')
      ax[1].set(xlabel='Displacement load (mm)', ylabel='Du (mm)')
      #ax[1].set_title('Normal Relative Displacements Evolution in a point of Interface')
      #ax[0].set_title('Tangential Relative Displacements Evolution in a point of Interface')
      
      atleat_partially_separated_locs=[]
      partially_separated_locs=np.array([])
      completely_separated_locs=np.array([])
      loaded_end_loc=np.where(nodes_data[:, 0] == nodes_data[-1, 0])[0][0] # first_decohesion_loc = loaded_end_loc
      completely_separated_locs=np.where(nodes_data[:,1+steps]==0)[0]

      for i in range(len(lines_interface_stresses)):
            list = nodes_data[i, 2:2+steps]
            index=np.argmax(list)
            if not index+1==steps:
                  atleat_partially_separated_locs.append(i)
      intacted_locs=np.array(sorted((Counter(np.arange(len(lines_interface_stresses))) - Counter(atleat_partially_separated_locs)).elements()))
      partially_separated_locs=np.array(sorted((Counter(atleat_partially_separated_locs) - Counter(completely_separated_locs)).elements()))  
      
      if completely_separated_locs.size == 0 and partially_separated_locs.size == 0:
            loc_to_plot=np.linspace(0, loaded_end_loc, 5).astype(int)
      elif completely_separated_locs.size == 0 and partially_separated_locs.size != 0:
            a=np.linspace(partially_separated_locs[0], partially_separated_locs[-1], 3).astype(int)
            b=np.linspace(intacted_locs[0], intacted_locs[-1], 3).astype(int)
            loc_to_plot=np.append(a,b)  
            loc_to_plot.sort()          
      elif completely_separated_locs.size != 0 and partially_separated_locs.size != 0:
            a=np.linspace(completely_separated_locs[0], completely_separated_locs[-1], 3).astype(int)
            b=np.linspace(partially_separated_locs[0], partially_separated_locs[-1], 3).astype(int)
            c=np.linspace(intacted_locs[0], intacted_locs[-1], 3).astype(int)
            loc_to_plot=np.append(a,b)
            loc_to_plot=np.append(loc_to_plot,c)
            loc_to_plot.sort()
      for n in loc_to_plot:
            dU = nodes_data[n, 2 + 3*steps:]
            dU = np.insert(dU, 0, 0)
            dV = nodes_data[n, 2+2*steps:2+3*steps]
            dV = np.insert(dV, 0, 0)
            if  completely_separated_locs.size!=0 and n in completely_separated_locs:
                  if n==completely_separated_locs[-1]: label=': first completely separated point'
                  elif n==completely_separated_locs[0]: label=': last completely separated point'
                  else: label=''
            elif  partially_separated_locs.size!=0 and n in partially_separated_locs:
                  if n==partially_separated_locs[-1]: label=': first partially separated point'
                  elif n==partially_separated_locs[0]: label=': last partially separated point'
                  else: label=''
            elif  intacted_locs.size!=0 and n in intacted_locs:
                  if n==intacted_locs[-1]: label=': first intacted point'
                  elif n==intacted_locs[0]: label=': last intacted point'
                  else: label=''
            else: label=''
            if n in intacted_locs: linestyle='dashed'
            else: linestyle='solid'
            ax[1].plot(Diss_load*1000, dU*1000, label='loc: y={:.2f}cm {}'.format(nodes_data[n, 1]*100, label), linewidth=0.6, linestyle=linestyle)
            ax[0].plot(Diss_load*1000, dV*1000, label='loc: y={:.2f}cm {}'.format(nodes_data[n, 1]*100, label), linewidth=0.6, linestyle=linestyle)
            dU_peaks_index = np.where((dU[1:-1] > dU[0:-2]) * (dU[1:-1] > dU[2:]))[0] + 1
            dU_peaks=dU[dU_peaks_index]
            Peaks_step=dU_peaks_index+1
      ax[0].legend(prop={'size': 5}, loc='upper left')
      savefig_nomargin(path, '6-Relative Displacements Evolution in a point of Interface')
      plt.close(fig)

      ######################################################################################################
      # plot 7: plotting Tangential and Normal tresses Evolution of Interface selected nodes   
      fig, ax = plt.subplots(2,1, sharex=True)
      #fig.suptitle('Stresses Evolution in a point of Interface')
      ax[0].set(ylabel=r'$\tau$ (MPa)')
      ax[1].set(xlabel='Displacement load (mm)', ylabel=r'$\sigma$ (MPa)')
      #ax[0].set_title('Interface Tangential Stress')
      #ax[1].set_title('Interface Normal Stress')
      for n in loc_to_plot:
            Sigma_tt = nodes_data[n, 2:2+steps]
            Sigma_tt = np.insert(Sigma_tt, 0, 0)
            Sigma_nn = nodes_data[n, 2+steps:2+2*steps]
            Sigma_nn = np.insert(Sigma_nn, 0, 0)
            if  completely_separated_locs.size!=0 and n in completely_separated_locs:
                  if n==completely_separated_locs[-1]: label=': first completely separated point'
                  elif n==completely_separated_locs[0]: label=': last completely separated point'
                  else: label=''
            elif  partially_separated_locs.size!=0 and n in partially_separated_locs:
                  if n==partially_separated_locs[-1]: label=': first partially separated point'
                  elif n==partially_separated_locs[0]: label=': last partially separated point'
                  else: label=''
            elif  intacted_locs.size!=0 and n in intacted_locs:
                  if n==intacted_locs[-1]: label=': first intacted point'
                  elif n==intacted_locs[0]: label=': last intacted point'
                  else: label=''
            else: label=''
            if n in intacted_locs: linestyle='dashed'
            else: linestyle='solid'
            ax[0].plot(Diss_load*1000, Sigma_tt, label='loc: y={:.2f}cm {}'.format(nodes_data[n, 1]*100, label), linewidth=0.6, linestyle=linestyle)
            ax[1].plot(Diss_load*1000, Sigma_nn, label='loc: y={:.2f}cm {}'.format(nodes_data[n, 1]*100, label), linewidth=0.6, linestyle=linestyle)
      ax[0].legend(prop={'size': 5}, loc='upper left')
      savefig_nomargin(path, '7-Stresses Evolution in a point of Interface')
      plt.close(fig)
      print('Detailed results of simulation {} saved in form of seven figures in \n {}'.format(simulation_name, path))
      

# function defining fig specification for plotting desired curves in one frame
def figspec_simresultploter_part2(axins_dim=[0.07, 0.77, 0.15, 0.15]):
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


# function which plots the Maxhoop stress, pullout curve, concrete reaction and yarn tensile stress un one fig for each simulation
def simresultploter_part2(ax1, ax1_1, ax1_2, axins, path):
    
    # assign path of monitor.csv 
    Monitor_dir_path = os.path.join(path, "AtenaCalculation/monitors.csv")
 
    # defining columns for panda dataframe based on monitors.csv / constructing monitors dataframe which includes all data of monitors.csv
    names=np.arange(0,100) # make it better to avoid unused space
    monitors = pd.read_csv(Monitor_dir_path, sep=';', names=names, skiprows=0)           ### start here
    # extracting lines in which stresses of interface nodes are stored from that line (for all steps)
    lines_interface_stresses=monitors.index[monitors[1].str.contains('MONITOR_SET_2_INTERFACE-STRESSES', case=True, na=False)].values


    # extracting total number of steps 
    steps=int(monitors[2].values[lines_interface_stresses[0]+2].strip())
 
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






