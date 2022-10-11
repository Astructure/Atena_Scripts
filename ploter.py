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
        
fig = plt.figure()
ax1 = fig.add_subplot(111)
ax1.set_title('Max Hoop Stress evolution')
ax1.set_ylabel('Mpa')
ax1.set_xlabel('Steps')

def ploter(name, color):
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
        plt.plot(steps, sigma_tt, color)
 
""" for name in names[0:150:30]:
        ploter(name ,'b')
for name in names[6:150:30]:
        ploter(name, 'r')
for name in names[12:150:30]:
        ploter(name,'g')
for name in names[18:150:30]:
        ploter(name,'c')
for name in names[24:150:30]:
        ploter(name,'k') """
        
        
        
""" for name in names[0:6:2]:
        ploter(name,'b') 
for name in names[6:12:2]:
        ploter(name,'r') 
for name in names[12:18:2]:
        ploter(name,'g') 
for name in names[18:24:2]:
        ploter(name,'c') 
for name in names[24:30:2]:
        ploter(name,'k')    """  
        
        
        
for name in names[0:2]:
        ploter(name,'b') 
for name in names[2:4]:
        ploter(name,'r') 
for name in names[4:6]:
        ploter(name,'g') 
for name in names[6:8]:
        ploter(name,'c') 
for name in names[8:10]:
        ploter(name,'k')     
        

plt.show()