import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
my_cols = ["A", "B", "C", "D", "E", "F", "G", "H"]
""" plt.rcParams["figure.figsize"] = [7.00, 3.50]
plt.rcParams["figure.autolayout"] = True
plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["font.size"] = 10
columns = ["Name", "Marks"] """

monitors = pd.read_csv(r'C:\Users\adelpasand\Desktop\axi\3D axi bond slip law (jump and slip) with monitoring.gid\AtenaCalculation\monitors.csv', sep=';', names=my_cols, skiprows=0)
""" pd.set_option('display.max_rows', df.shape[0]+1)
 """

""" values = np.array(monitors['D'][monitors.index[monitors['B'].str.contains('PIN_NORMAL_FORCE_', na=False)].values + 7]).astype(
        float)  # +7 so that we take the correct row - if we have 1 time step, 1 iteration, if not, check monitors """
print(monitors.index[monitors['B'].str.contains('Time', case=True, na=False)].values)

""" plt.plot(df.Name, df.Marks)
plt.show() """