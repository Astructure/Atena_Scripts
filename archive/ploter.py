import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os


output_dir = "C:/Users/adelpasand/Desktop/p study" 
os.chdir(output_dir)

def model_number_spliter(ele):
        number , name = ele.split('_', 1)
        return int(number)

if os.path.isdir(output_dir):
       names=os.listdir(".")
       names.sort(key=model_number_spliter)
else:
        print("there is no directory as an storage for runned-models")
        


def reader(name):
        path = os.path.join(output_dir, name, 'AtenaCalculation', 'monitors.csv') 
        print(name)
        my_cols = ["A", "B", "C", "D", "E", "F", "G", "H"]
        monitors = pd.read_csv(path, sep=';', names=my_cols, skiprows=0)
        if monitors.index[monitors['D'].str.contains('sigma_tt', case=True, na=False)].size==0:
                print("there is no monitor defined for sigma_tt")
        else:
                line=int(monitors.index[monitors['D'].str.contains('sigma_tt', case=True, na=False)].values)
                unit=''.join(monitors['D'].values[line+1]).strip()
                step_n=int(monitors['C'][monitors.index[monitors['B'].str.contains('Step', case=True, na=False)].values[0]])
                steps=monitors['C'].values[line+2:line+3+step_n].astype(float)
                if ''.join(monitors['D'].values[line+2]).strip() == "NaN":
                        sigma_tt=monitors['D'].values[line+3:line+3+step_n].astype(float)
                        sigma_tt=np.insert(sigma_tt, 0, 0)
                else:
                        sigma_tt=monitors['D'].values[line+2:line+3+step_n].astype(float)
        return steps, sigma_tt
        

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