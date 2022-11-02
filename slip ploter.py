
from turtle import Shape
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

path = "C:/Users/adelpasand/Desktop/axi/3D axiii2.gid/AtenaCalculation/monitors.csv" 
my_cols = ["A", "B", "C", "D", "E", "F", "G", "H"]
monitors = pd.read_csv(path, sep=';', names=my_cols, skiprows=0)


line=monitors.index[monitors['B'].str.contains('INTERFACE_DISPLACEMENTS #101000', case=True, na=False)].values
print(line)

for count, line in enumerate(line,start=1)
    if ''.join(monitors['D'].values[line[0]+6]).strip() == "NaN":
            Slip_N=monitors['D'].values[line[0]+7:line[0]+57].astype(float)
            Slip_N=np.insert(Slip_N, 0, 0)
    else:
            Slip_N=monitors['D'].values[line[0]+6:line[0]+57].astype(float)
        
    print(Slip_N)

nodes = list(range(1, 502))

fig, axs = plt.subplots(2, 2)
 
axs[0,0].plot(Slip_N, nodes)
plt.show()