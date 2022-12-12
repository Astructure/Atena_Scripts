import matplotlib.pyplot as plt
import numpy as np

def PS1():
    ratio=2 # ratio = G_f/G_o #bilnear CZL
    C_0= [1,2,3]
    Ktt=5000
    phi=0.3
    fig, axs = plt.subplots()
    fig.suptitle('Interface Traction Separation Law (Gf = {} Go)'.format(ratio))
    axs.set(xlabel='Dv (sliding) (mm)', ylabel='Shear Stress (MPa)')
    fig, ax = plt.subplots()
    fig.suptitle('Threshold surface')
    ax.set(xlabel='Normal stress (MPa)', ylabel='Tangential stress (MPa)')
    ax.axvline(x=0 , linestyle='dashed', color='k', linewidth=0.5)
    ax.axhline(y=0 , linestyle='dashed', color='k', linewidth=0.5)
    #ax.grid(color='k', linestyle='-', linewidth=0.1)
    #ax.axis('equal')
    for i, value in enumerate(C_0):
        DV1=np.linspace(0,C_0[i]*1000/Ktt,10)
        DV2=np.linspace(C_0[i]*1000/Ktt,(ratio)*C_0[i]*1000/Ktt,11)
        DV2=np.delete(DV2,0)
        DV=np.append(DV1, DV2)
        tau1=np.linspace(0,C_0[i],10)
        tau2=np.linspace(C_0[i],0,11)
        tau2=np.delete(tau2, 0)
        tau=np.append(tau1,tau2)
        axs.plot(DV, tau, label='C={} , Ktt={} MN/m3'.format(value,Ktt))
        axs.fill_between(DV1, tau1, alpha=0.05 , label='G_o={} N/m (J/m^2)'.format(C_0[i]*C_0[i]*1E6/Ktt))
        c = C_0[i]
        ft = c
        #ft = np.linspace(c/4,c,4)
        #for ft in ft:
        sigma_ell=np.linspace(0,ft,100)
        sigma_c=-phi*ft**2/(c-2*ft*phi)
        tau0=c/(1-(sigma_c**2/(ft-sigma_c)**2))**0.5
        tau_ell=tau0*(1-((sigma_ell-sigma_c)/(ft-sigma_c))**2)**0.5
        sigma_lin=np.linspace(0,-2*max(C_0),10)
        sigma_lin=np.delete(sigma_lin,0)
        tau_lin=c-sigma_lin*phi
        sigma=np.append(sigma_lin,sigma_ell)
        tau=np.append(tau_lin,tau_ell)
        ax.plot(sigma,tau, color='b',linewidth=0.8)
        ax.plot(sigma_ell,sigma_ell, color='b',linewidth=0.8)
    axs.legend(prop={'size': 8})
    return axs


ratio=2 # ratio = G_f/G_o
C_0= 1 
Ktt=[5000,5000/2,5000/3]
fig, axs = plt.subplots()
fig.suptitle('Interface Traction Separation Law (Gf = {} Go)'.format(ratio))
axs.set(xlabel='Dv (sliding) (mm)', ylabel='Shear Stress (MPa)')
for i, value in enumerate(Ktt):
    DV1=np.linspace(0,C_0*1000/Ktt[i],10)
    DV2=np.linspace(C_0*1000/Ktt[i],(ratio)*C_0*1000/Ktt[i],11)
    DV2=np.delete(DV2,0)
    DV=np.append(DV1, DV2)
    tau1=np.linspace(0,C_0,10)
    tau2=np.linspace(C_0,0,11)
    tau2=np.delete(tau2, 0)
    tau=np.append(tau1,tau2)
    axs.plot(DV, tau, label='C= 1 MPa, Ktt= {:.2f} MN/m3'.format(value))
    axs.fill_between(DV1, tau1, alpha=0.05 , label='G_o={} N/m (J/m^2)'.format(C_0*C_0*1E6/Ktt[i]))
axs.legend(prop={'size': 8})


ratio=2 # ratio = G_f/G_o
C_0_min= 1 
C_0_Max= 3
Ktt=5000
r=np.linspace(1,C_0_Max/C_0_min,3)
C_0=r*C_0_min
Ktt=r*Ktt
fig, axs = plt.subplots()
fig.suptitle('Interface Traction Separation Law (Gf = {} Go)'.format(ratio))
axs.set(xlabel='Dv (sliding) (mm)', ylabel='Shear Stress (MPa)')
for i, value in enumerate(r):
    DV1=np.linspace(0,C_0[i]*1000/Ktt[i],10)
    DV2=np.linspace(C_0[i]*1000/Ktt[i],(ratio)*C_0[i]*1000/Ktt[i],11)
    DV2=np.delete(DV2,0)
    DV=np.append(DV1, DV2)
    tau1=np.linspace(0,C_0[i],10)
    tau2=np.linspace(C_0[i],0,11)
    tau2=np.delete(tau2, 0)
    tau=np.append(tau1,tau2)
    axs.plot(DV, tau, label='C={} MPa , Ktt={} MN/m3'.format(C_0[i],Ktt[i]))
    axs.fill_between(DV1, tau1, alpha=0.05 , label='G_o={} N/m (J/m^2)'.format(C_0[i]*C_0[i]*1E6/Ktt[i]))
axs.legend(prop={'size': 8})

ratio=[1, 1.5 ,2, 3]
C_ratio=1.4
C_0= 2 
C_1=C_ratio*C_0
Ktt=5000
fig, axs = plt.subplots()
fig.suptitle('Interface Traction Separation Law (G_o={} N/m (J/m^2))'.format(C_0*C_0*1E6/Ktt))
axs.set(xlabel='Dv (sliding) (mm)', ylabel='Shear Stress (MPa)')
for i, value in enumerate(ratio):
    DV1=np.linspace(0,C_0*1000/Ktt,10)
    DV2=np.linspace(C_0*1000/Ktt,(ratio[i])*C_0*1000/Ktt,11)
    DV2=np.delete(DV2,0)
    DV=np.append(DV1, DV2)
    tau1=np.linspace(0,C_0,10)
    tau2=np.linspace(C_0,0,11)
    tau2=np.delete(tau2, 0)
    tau=np.append(tau1,tau2)
    axs.plot(DV, tau, label='C={} MPa , Ktt={} MN/m3, Gf/Go={}'.format(C_0,Ktt,ratio[i]))
    axs.fill_between(DV1, tau1, alpha=0.05)
    if value == ratio[-1]:
        tau2=np.linspace(C_0,C_1,11)
        tau2=np.delete(tau2, 0)
        tau=np.append(tau1,tau2)
        axs.plot(DV, tau, label='C={} MPa , Ktt={} MN/m3, Gf/Go={}'.format(C_0,Ktt,2*ratio[i]-1))   
        tau2=np.linspace(C_0,C_0,11)
        tau2=np.delete(tau2, 0)
        tau=np.append(tau1,tau2)
        axs.plot(DV, tau, label='C={} MPa , Ktt={} MN/m3, Gf/Go={:.2f}'.format(C_0,Ktt,1+0.5*(C_0+C_1)*(ratio[i]-1)))  
axs.legend(prop={'size': 8})

fig, axs = plt.subplots()
fig.suptitle('Interface Traction Separation Law')
axs.set(xlabel='Du (Opening) (mm)', ylabel='Normal Stress (MPa)')
F_t= 1
Knn=5000
alpha2=1
DU1=np.linspace(0,F_t*1000/Knn,10)
DU2=np.linspace(F_t*1000/Knn,(1+alpha2)*F_t*1000/Knn,11)
DU2=np.delete(DU2,0)
DU=np.append(DU1,DU2)
sigma1=np.linspace(0,F_t,10)
sigma2=np.linspace(F_t,0,11)
sigma2=np.delete(sigma2,0)
sigma=np.append(sigma1, sigma2)
axs.plot(DU, sigma)
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
axs.text(0.05, 0.95, 'Knn=5000 MN/m3', transform=axs.transAxes, fontsize=14,
        verticalalignment='top', bbox=props)


fig, axs = plt.subplots()
fig.suptitle('FRP yarn material model')
axs.set(xlabel='strain (%)', ylabel='Stress (GPa)')
Ft= 3.3
E=230
strain=np.linspace(0,Ft/E,10)*100
Stress=np.linspace(0,Ft,10)
axs.plot(strain, Stress)
xmax = strain.max()
ymax = Stress.max()
X_extraticks=[xmax]
Y_extraticks=[ymax]
secax_x = axs.secondary_xaxis('top')
secax_x.set_xticks(X_extraticks)
secax_y = axs.secondary_yaxis('right')
secax_y.set_yticks(Y_extraticks)
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
axs.text(0.05, 0.95, 'E=230 GPa ; v=0.2', transform=axs.transAxes, fontsize=14,
        verticalalignment='top', bbox=props)
plt.show()
