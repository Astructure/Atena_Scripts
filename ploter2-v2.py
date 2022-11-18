import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os


# function which can read inp file
def inp_reader(file_path):
    with open(file_path, 'r') as file:
            data = file.readlines()
    return data

# assign path of monitor.csv 
Monitor_dir_path = "C:/Users/adelpasand/Desktop/axi/axi-Diss controlled with softening in Ktt- 1mm 150 step try.gid/AtenaCalculation/monitors.csv"  
# assign path of inp file (.inp )
Inp_dir_path = "C:/Users/adelpasand/Desktop/axi/axi-Diss controlled with softening in Ktt- 1mm 150 step try.gid/AtenaCalculation/axi-Diss controlled with softening in Ktt- 1mm 150 step try.inp"  

# all data included in .inp file are stored in the variable inp_data 
inp_data=inp_reader(Inp_dir_path)

# extracting total number of nodes and corresponding coordinates
for line in inp_data:
    if line.find('Coordinate definition. Suma=') != -1:
        number_of_nodes=int(inp_data[inp_data.index(line)].split("=",1)[1].strip())
        node_coords = pd.DataFrame(inp_data[inp_data.index(line)+2:inp_data.index(line)+number_of_nodes+2])
        node_coords=node_coords[0].str.split(expand = True)

# defining columns for panda dataframe based on monitors.csv / costructing monitors dataframe which includes all data of monitors.csv
monitors_cols = ["A", "B", "C", "D", "E", "F", "G", "H"]
monitors = pd.read_csv(Monitor_dir_path, sep=';', names=monitors_cols, skiprows=0)

# extracting lines in which stresses of interface nodes are stored from that line (for all steps)
lines_interface_stresses=monitors.index[monitors['B'].str.contains('MONITOR_SET_2_INTERFACE-STRESSES', case=True, na=False)].values

# extracting lines in which diss of interface nodes are stored from that line (for all steps)
lines_interface_diss=monitors.index[monitors['B'].str.contains('MONITOR_SET_2_INTERFACE-DISS', case=True, na=False)].values

# extracting interface node ID and coordinates
interface_nodes_id=pd.DataFrame(monitors['B'].values[lines_interface_stresses[0:len(lines_interface_stresses)]])
interface_nodes_id=pd.to_numeric(interface_nodes_id[0].str.split(pat="_", expand = True)[4])
interface_nodes_coords=np.array(node_coords.iloc[interface_nodes_id-1])
y_coord=np.array(interface_nodes_coords[:, 2],dtype=np.float_)
x_coord=np.array(interface_nodes_coords[:, 1],dtype=np.float_)
interface_nodes_id=np.array(interface_nodes_coords[:, 0],dtype=np.int_) #Defined again to be sure that the order of data remains unchanged

# extracting total number of steps 
steps=int(monitors['C'].values[lines_interface_stresses[0]+2].strip())

# constructing a 2D array containing interface nodes data including node ID, Y-coordinates, stress, and relative displacement in the tangential and normal direction
nodes_data = np.zeros((len(lines_interface_stresses), 2 + 4*steps))
nodes_data[:, 0] = interface_nodes_id
nodes_data[:, 1] = y_coord
for i in range(len(lines_interface_stresses)):
    Sigma_tt = np.array(monitors['D'].values[lines_interface_stresses[i]+7:lines_interface_stresses[i]+7+steps], dtype=np.float_)
    Sigma_nn = np.array(monitors['E'].values[lines_interface_stresses[i]+7:lines_interface_stresses[i]+7+steps], dtype=np.float_)
    dV = np.array(monitors['D'].values[lines_interface_diss[i]+7:lines_interface_diss[i]+7+steps], dtype=np.float_)
    dU = np.array(monitors['E'].values[lines_interface_diss[i]+7:lines_interface_diss[i]+7+steps], dtype=np.float_)
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

# plotting Tangential and Normal Stress profile along the interface
fig, axs = plt.subplots(2)
fig.suptitle('Stress profile along the interface')
axs[0].set_title('Interface Tangential Stress')
axs[1].set_title('Interface Normal Stress ')
axs[1].set(xlabel='interface length (cm)')
axs[1].set(ylabel='MPa')
axs[0].set(ylabel='MPa')
fig.set_figheight(7)
fig.set_figwidth(6)
x_coords = nodes_data[:, 1]

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

for s in step_to_plot:
      Sigma_tt = nodes_data[:, 2 + s-1]
      Sigma_nn = nodes_data[:, 2 + steps + s-1]
      label, linestyle=label_linewidth(s)
      axs[0].plot(x_coords*100, Sigma_tt, label=label, linewidth=0.8, linestyle=linestyle)
      axs[1].plot(x_coords*100, Sigma_nn, label=label, linewidth=0.8, linestyle=linestyle)
axs[0].legend(prop={'size': 6}, loc='upper left')
      
# plotting Tangential and Normal Relative Displacements profile along the Interface
fig, axs = plt.subplots(2)
fig.suptitle('Relative Displacements profile along the Interface')
axs[1].set_title('Normal Relative Displacement (opening)')
axs[0].set_title('Tangential Relative Displacements (sliding)')
axs[1].set(xlabel='Interface Length (cm)', ylabel='mm')
axs[0].set(ylabel='mm')
fig.set_figheight(7)
fig.set_figwidth(7)
for s in step_to_plot:
      dV = nodes_data[:, 2 + 2*steps +s-1]
      dU = nodes_data[:, 2 + 3*steps + s-1]
      label, linestyle=label_linewidth(s)
      axs[1].plot(x_coords*100, dU*1000, label=label ,linewidth=0.8, linestyle=linestyle)
      axs[0].plot(x_coords*100, dV*1000, label=label ,linewidth=0.8, linestyle=linestyle)
axs[0].legend(prop={'size': 6}, loc='upper left')


# plotting Relative Opening of Interface with respect to fixed end and with respect to loaded end'
fig, axs = plt.subplots(2)
fig.suptitle('Relative Opening of Interface')
axs[0].set_title('with respect to fixed end')
axs[1].set_title('with respect to loaded end')
axs[1].set(xlabel='Interface Length (cm)', ylabel='mm')
axs[0].set(ylabel='mm')
fig.set_figheight(7)
fig.set_figwidth(7)
for s in step_to_plot:
      startshifted_dU = nodes_data[:, 2 + 3*steps + s-1]-nodes_data[0, 2 + 3*steps + s-1]
      endshifted_dU = nodes_data[:, 2 + 3*steps + s-1]-nodes_data[-1, 2 + 3*steps + s-1]
      label, linestyle=label_linewidth(s)
      axs[0].plot(x_coords*100, startshifted_dU, label=label , linewidth=0.8 , linestyle=linestyle)
      axs[1].plot(x_coords*100, endshifted_dU, label=label , linewidth=0.8, linestyle=linestyle)
axs[0].legend(prop={'size': 6}, loc='upper left')


# plotting Normalized Opening of Interface with respect to fixed end and with respect to loaded end'
fig, axs = plt.subplots(2)
fig.suptitle('Normalized Opening of Interface')
axs[0].set_title('with respect to fixed end')
axs[1].set_title('with respect to loaded end')
axs[1].set(xlabel='Interface Length (cm)', ylabel='_')
axs[0].set(ylabel='_')
fig.set_figheight(7)
fig.set_figwidth(7)
for s in step_to_plot:
      start_normalized_dU = nodes_data[:, 2 + 3*steps + s-1]/nodes_data[0, 2 + 3*steps + s-1]
      end_normalized_dU = nodes_data[:, 2 + 3*steps + s-1]/nodes_data[-1, 2 + 3*steps + s-1]
      label, linestyle=label_linewidth(s)
      axs[0].plot(x_coords*100, start_normalized_dU, label=label , linewidth=0.8, linestyle=linestyle)
      axs[1].plot(x_coords*100, end_normalized_dU, label=label , linewidth=0.8, linestyle=linestyle)
axs[0].legend(prop={'size': 6}, loc='upper left')

# plotting Normal Relative Displacements of Interface(opening) for all steps. focus is on profile evolution and zoom in on the loaded end opening
fig, ax = plt.subplots(1,2, figsize=(12,7), gridspec_kw={'width_ratios': [2, 1]})
fig.suptitle('Normal Relative Displacements of Interface (opening)')
ax[0].set(xlabel='Interface Length (cm)', ylabel='mm')
ax[0].set(xlabel='Interface Length (cm)', ylabel='mm')
for s in range(1,steps+1):
      dU = nodes_data[:, 2 + 3*steps + s-1]
      if s==critical_load_step: 
            label='Step {}: critical load step'.format(s)
            linewidth=1.2
      elif  s==critical_load_step+1: 
            label='Step {}: decohesion initiation load step'.format(s)
            linewidth=1.2
      elif  s==steps: 
            label='Step {}: last load step'.format(s)
            linewidth=1.2
      else: 
            label=''
            linewidth=0.4
      if s <= critical_load_step: linestyle='dashed'
      else: linestyle='solid'  
      ax[0].plot(x_coords*100, dU*1000, label=label, linewidth=linewidth, linestyle=linestyle)
rect=mpatches.Rectangle((4.9,0.001650),0.1,0.00021,fill = False, color = "black", linewidth = 0.8)
ax[0].add_patch(rect)
ax[0].legend(prop={'size': 6}, loc='upper left')     
ax[1].set_xlim([4.9, 5.01])
ax[1].set_ylim([.00165, .00186])
step_to_plot_p1=np.arange(critical_load_step-3, critical_load_step+1)
step_to_plot_p2=np.arange(critical_load_step+1, critical_load_step+13)
step_to_plot=np.append(step_to_plot_p1,step_to_plot_p2)
for s in step_to_plot:
      dU = nodes_data[:, 2 + 3*steps + s-1]
      label, linewidth=label_linewidth(s)
      ax[1].plot(x_coords*100, dU*1000, label=label ,linewidth=0.8, linestyle=linestyle)
ax[1].legend(prop={'size': 6}, loc='lower right')       
      
steps_array=np.arange(0,steps+1)

# Tangential and Normal Relative Displacements Evolution of Interface selected nodes   
step_to_plot=range(1,steps)   # Enter steps you want to consider for plotting. acceptable rang from 1 to steps
fig, ax = plt.subplots(2)
fig.suptitle('Relative Displacements Evolution in a point of Interface')
ax[0].set(ylabel='mm')
ax[1].set(xlabel='Step', ylabel='mm')
ax[1].set_title('Normal Relative Displacements Evolution in a point of Interface')
ax[0].set_title('Tangential Relative Displacements Evolution in a point of Interface')
fig.set_figheight(7)
fig.set_figwidth(7)
last_decohesion_loc=np.where(nodes_data[:,1+steps]==0)[0][0]
first_decohesion_loc=np.where(nodes_data[:, 0] == nodes_data[-1, 0])[0][0] # first_decohesion_loc = loaded_end_loc
loc_to_plot=[first_decohesion_loc, last_decohesion_loc, 0, int((last_decohesion_loc+first_decohesion_loc)/2),int((0+last_decohesion_loc)/2), first_decohesion_loc-4]
loc_to_plot.sort()
for n in loc_to_plot:
      dU = nodes_data[n, 2 + 3*steps:]
      dU = np.insert(dU, 0, 0)
      dV = nodes_data[n, 2+2*steps:2+3*steps]
      dV = np.insert(dV, 0, 0)
      if n==first_decohesion_loc: label=': loaded_end_loc = first_decohesion_loc'
      elif  n==last_decohesion_loc: label=': last_decohesion_loc'
      elif  n==0: label='fixed_end_loc'
      else: label=''
      if n < last_decohesion_loc: linestyle='dashed'
      else: linestyle='solid'
      ax[1].plot(steps_array, dU*1000, label='y={} {}'.format(nodes_data[n, 1], label), linewidth=0.8, linestyle=linestyle)
      ax[0].plot(steps_array, dV*1000, label='y={} {}'.format(nodes_data[n, 1], label), linewidth=0.8, linestyle=linestyle)
      dU_peaks_index = np.where((dU[1:-1] > dU[0:-2]) * (dU[1:-1] > dU[2:]))[0] + 1
      dU_peaks=dU[dU_peaks_index]
      Peaks_step=dU_peaks_index+1
      extraticks=[125]
      ax[0].legend(prop={'size': 7}, loc='upper left')

# plotting Tangential and Normal tresses Evolution of Interface selected nodes   
fig, ax = plt.subplots(2)
fig.suptitle('Stresses Evolution in a point of Interface')
ax[0].set(ylabel='MPa')
ax[1].set(xlabel='Step', ylabel='MPa')
ax[0].set_title('Interface Tangential Stress')
ax[1].set_title('Interface Normal Stress')
fig.set_figheight(7)
fig.set_figwidth(7)
for n in loc_to_plot:
      Sigma_tt = nodes_data[n, 2:2+steps]
      Sigma_tt = np.insert(Sigma_tt, 0, 0)
      Sigma_nn = nodes_data[n, 2+steps:2+2*steps]
      Sigma_nn = np.insert(Sigma_nn, 0, 0)
      if n==first_decohesion_loc: label=': loaded_end_loc = first_decohesion_loc'
      elif  n==last_decohesion_loc: label=': last_decohesion_loc'
      elif  n==0: label='fixed_end_loc'
      else: label=''
      if n < last_decohesion_loc: linestyle='dashed'
      else: linestyle='solid'
      ax[0].plot(steps_array, Sigma_tt, label='y={} {}'.format(nodes_data[n, 1], label), linewidth=0.8, linestyle=linestyle)
      ax[1].plot(steps_array, Sigma_nn, label='y={} {}'.format(nodes_data[n, 1], label), linewidth=0.8, linestyle=linestyle)
      ax[0].legend(prop={'size': 7}, loc='upper left')



# plotting Max Hoop stress evolution in concrete (Mpa)
if monitors.index[monitors['D'].str.contains('sigma_tt', case=True, na=False)].size==0:
      print("there is no monitor defined for max hoop stress in concrete")
else:
      line_maxhoop=int(monitors.index[monitors['D'].str.contains('sigma_tt', case=True, na=False)].values)
      unit=''.join(monitors['D'].values[line_maxhoop+1]).strip()
      if ''.join(monitors['D'].values[line_maxhoop+2]).strip() == "NaN":
            sigma_tt=monitors['D'].values[line_maxhoop+3:line_maxhoop+3+steps].astype(float)
            sigma_tt=np.insert(sigma_tt, 0, 0)
      else:
            sigma_tt=monitors['D'].values[line_maxhoop+2:line_maxhoop+3+steps].astype(float)
fig, axs = plt.subplots()
fig.suptitle('Max Hoop Stress evolution in concrete')
axs.set(xlabel='Load Steps', ylabel='Max Hoop stress (Mpa)')
axs.plot(steps_array, sigma_tt)
xmax = steps_array[np.argmax(sigma_tt)]
ymax = sigma_tt.max()
# axs.plot((xmax, xmax), (0, ymax), linewidth=0.4 , linestyle='dashed' , color='k')
X_extraticks=[xmax]
Y_extraticks=[ymax]
secax_x = axs.secondary_xaxis('top')
secax_x.set_xticks(X_extraticks)
secax_y = axs.secondary_yaxis('right')
secax_y.set_yticks(Y_extraticks)

plt.show()
