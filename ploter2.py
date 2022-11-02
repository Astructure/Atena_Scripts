import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os


def inp_reader(file_path):
    with open(file_path, 'r') as file:
            data = file.readlines()
    return data


Monitor_dir_path = "C:/Users/adelpasand/Desktop/axi/3D axi-final load controlled - 1.5 percent strain 150 step.gid/AtenaCalculation/monitors.csv"  
Inp_dir_path = "C:/Users/adelpasand/Desktop/axi/3D axi-final load controlled - 1.5 percent strain 150 step.gid/AtenaCalculation/3D axi-final load controlled - 1.5 percent strain 150 step.inp"  
inp=inp_reader(Inp_dir_path)

coordinates = []

for lines_nums in inp:
    if lines_nums.find('JOINT COORDINATES') != -1:
        nodes=int(inp[inp.index(lines_nums)-1].split("=",1)[1].strip())
        data = pd.DataFrame(inp[inp.index(lines_nums)+1:inp.index(lines_nums)+nodes+1])
        data=data[0].str.split(expand = True)
monitors_cols = ["A", "B", "C", "D", "E", "F", "G", "H"]
monitors = pd.read_csv(Monitor_dir_path, sep=';', names=monitors_cols, skiprows=0)


indices_of_node_lines = monitors['B'].str.contains('MONITOR_SET_2_INTERFACE-STRESSES', case=True, na=False)
if monitors.index[indices_of_node_lines].size==0:
        print("there is no monitor defined for INTERFACE-STRESSES")
else:
        lines_nums=monitors.index[indices_of_node_lines].values
        node_nums=pd.DataFrame(monitors['B'].values[lines_nums[0:len(lines_nums)]])
        node_nums=pd.to_numeric(node_nums[0].str.split(pat="_", expand = True)[4])
        interface_nodes_coord=data.iloc[node_nums]
        x=interface_nodes_coord[2]
        print(lines_nums)
        print(x)
        print(interface_nodes_coord)
       

step=int(monitors['C'].values[lines_nums[0]+2].strip())

nodes_data = np.zeros((len(lines_nums), 2 + step))

nodes_data[:, 0] = np.array(node_nums)


nodes_data[:, 1] = np.array(x, dtype=np.float_)

for i in range(step):
    arr = np.array(pd.DataFrame(monitors['D'].values[lines_nums[i]+7:lines_nums[i]+7+step], columns=[node_nums[i]]))
    nodes_data[i, 2:] =np.transpose(arr)

step_to_plot = 0
x_coords = nodes_data[0]
sigs = nodes_data[0, 2 + step_to_plot]


# Sig_tt=pd.DataFrame(monitors['D'].values[lines_nums[0]+7:lines_nums[0]+7+step], columns=[node_nums[0]])

Sig_t=pd.to_numeric(monitors['D'].values[lines_nums[0]+7:lines_nums[0]+7+step])
Sig_n=pd.to_numeric(monitors['E'].values[lines_nums[0]+7:lines_nums[0]+7+step])


"""         unit=''.join(monitors['D'].values[line+1]).strip()
        step_n=int(monitors['C'][monitors.index[monitors['D'].str.contains('Step', case=True, na=False)].values[0]])
        steps=monitors['C'].values[line+2:line+3+step_n].astype(float)
        if ''.join(monitors['D'].values[line+2]).strip() == "NaN":
                sigma_tt=monitors['D'].values[line+3:line+3+step_n].astype(float)
                sigma_tt=np.insert(sigma_tt, 0, 0)
        else:
                sigma_tt=monitors['D'].values[line+2:line+3+step_n].astype(float) """
        
"""
def annot_max(x,y, ax=None):
    xmax = x[np.argmax(y)]
    ymax = y.max()
    text= "x={:.0f}, y={:.3f}".format(xmax, ymax)
    if not ax:
        ax=plt.gca()
    bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
    arrowprops=dict(arrowstyle="->",connectionstyle="angle,angleA=0,angleB=60")
    kw = dict(xycoords='data',textcoords="axes fraction",
              arrowprops=arrowprops, bbox=bbox_props, ha="right", va="top")
    ax.annotate(text, xy=(xmax, ymax), xytext=(0.94,0.96), **kw)

        
        
        
fig, axs = plt.subplots(2, 3)
fig.delaxes(axs[1,2])
fig.suptitle('Max Hoop Stress evolution')
for ax in axs.flat:
    ax.set(xlabel='Steps', ylabel='Mpa')
for ax in axs.flat:
    ax.label_outer()
 
for name in names[0:30:6]:
      steps, sigma_tt = reader(name)
      axs[0,0].plot(steps, sigma_tt)
      axs[0,0].set_title('K_tt=5000 MN/m3')
annot_max(steps,sigma_tt,axs[0,0])   

for name in names[30:60:6]:
      steps, sigma_tt = reader(name)
      axs[0,1].plot(steps, sigma_tt)
      axs[0,1].set_title('K_tt=6750 MN/m3')
annot_max(steps,sigma_tt,axs[0,1])   

for name in names[60:90:6]:
      steps, sigma_tt = reader(name)
      axs[0,2].plot(steps, sigma_tt)
      axs[0,2].set_title('K_tt=8500 MN/m3')
annot_max(steps,sigma_tt,axs[0,2])   
     
for name in names[90:120:6]:
      steps, sigma_tt = reader(name)
      axs[1,0].plot(steps, sigma_tt)
      axs[1,0].set_title('K_tt=10250 MN/m3')
annot_max(steps,sigma_tt,axs[1,0])   

      
for name in names[120:150:6]:
      steps, sigma_tt = reader(name)
      axs[1,1].plot(steps, sigma_tt)
      axs[1,1].set_title('K_tt=12000 MN/m3')
annot_max(steps,sigma_tt,axs[1,1])   

      




fig, axs = plt.subplots()
fig.suptitle('Max Hoop Stress evolution')
axs.set(xlabel='Steps', ylabel='Mpa')
      
for name in names[0:30:6]:
      steps, sigma_tt = reader(name)
      axs.plot(steps, sigma_tt, 'b')

for name in names[30:60:6]:
      steps, sigma_tt = reader(name)
      axs.plot(steps, sigma_tt, 'r')
      
for name in names[60:90:6]:
      steps, sigma_tt = reader(name)
      axs.plot(steps, sigma_tt, 'g')
      
for name in names[90:120:6]:
      steps, sigma_tt = reader(name)
      axs.plot(steps, sigma_tt, 'c')
      
for name in names[120:150:6]:
      steps, sigma_tt = reader(name)
      axs.plot(steps, sigma_tt, 'k')
      
 """
 
 
 
 
""" for name in names[0:150:30]:
      steps, sigma_tt = reader(name)
      axs[0,0].plot(steps, sigma_tt)

for name in names[6:150:30]:
      steps, sigma_tt = reader(name)
      axs[0,1].plot(steps, sigma_tt)
      
for name in names[12:150:30]:
      steps, sigma_tt = reader(name)
      axs[0,2].plot(steps, sigma_tt)
      
for name in names[18:150:30]:
      steps, sigma_tt = reader(name)
      axs[1,0].plot(steps, sigma_tt)
      
for name in names[24:150:30]:
      steps, sigma_tt = reader(name)
      axs[1,1].plot(steps, sigma_tt) """
        
        
        
""" for name in names[0:6:2]:
      steps, sigma_tt = reader(name)
      axs[0,0].plot(steps, sigma_tt)
for name in names[6:12:2]:
      steps, sigma_tt = reader(name)
      axs[0,1].plot(steps, sigma_tt)
for name in names[12:18:2]:
      steps, sigma_tt = reader(name)
      axs[0,2].plot(steps, sigma_tt)
for name in names[18:24:2]:
      steps, sigma_tt = reader(name)
      axs[1,0].plot(steps, sigma_tt)
for name in names[24:30:2]:
      steps, sigma_tt = reader(name)
      axs[1,1].plot(steps, sigma_tt) """
        
        
        
""" for name in names[0:2]:
        ploter(name,'b') 
for name in names[2:4]:
        ploter(name,'r') 
for name in names[4:6]:
        ploter(name,'g') 
for name in names[6:8]:
        ploter(name,'c') 
for name in names[8:10]:
        ploter(name,'k')     
         """


plt.show()