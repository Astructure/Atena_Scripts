import matplotlib.pyplot as plt
import numpy as np

def biliner_TSL(C_0,Ktt,ratio):
    # ratio = G_f/G_o #bilnear CZL
    DV1=np.linspace(0,C_0*1000/Ktt,10)
    DV2=np.linspace(C_0*1000/Ktt,(ratio)*C_0*1000/Ktt,11)
    DV2=np.delete(DV2,0)
    DV=np.append(DV1, DV2)
    tau1=np.linspace(0,C_0,10)
    tau2=np.linspace(C_0,0,11)
    tau2=np.delete(tau2, 0)
    tau=np.append(tau1,tau2)
    return DV, DV1, tau, tau1

def bilin_TSL_ploter(fig, ax, C_0, Ktt, ratio, hatch ='false'):
    DV,DV1,tau,tau1 = biliner_TSL(C_0,Ktt,ratio)
    ax.plot(DV, tau, label='C0={} MPa , Ktt={} MN/m3, Gf/Go = {}'.format(C_0, 
        int(Ktt) if float(Ktt).is_integer() else "{:.2f}".format(Ktt), ratio))
    if hatch =='true':
        ax.fill_between(DV1, tau1, alpha=0.05 , label='G_o={} N/m (J/m^2)'.format(C_0*C_0*1E6/Ktt))
    ax.legend(prop={'size': 8})   

    
def plateau_TSL(C_0,Ktt,ratio):
    # ratio = G_f/G_o #plateau CZL
    DV1=np.linspace(0,C_0*1000/Ktt,10)
    DV2=np.linspace(C_0*1000/Ktt,0.5*(ratio+1)*C_0*1000/Ktt,11)
    DV2=np.delete(DV2,0)
    DV=np.append(DV1, DV2)
    tau1=np.linspace(0,C_0,10)
    tau2=np.linspace(C_0,C_0,11)
    tau2=np.delete(tau2, 0)
    tau=np.append(tau1,tau2)
    return DV, DV1, tau, tau1

def plateau_TSL_ploter(fig, ax, C_0, Ktt, ratio, hatch='false'):
    DV,DV1,tau,tau1 = plateau_TSL(C_0,Ktt,ratio)
    ax.plot(DV, tau, label='C0={} MPa , Ktt={} MN/m3, Gf/Go = {}'.format(C_0, 
        int(Ktt) if float(Ktt).is_integer() else "{:.2f}".format(Ktt), ratio))
    if hatch =='true':
        ax.fill_between(DV1, tau1, alpha=0.05 , label='G_o={} N/m (J/m^2)'.format(C_0*C_0*1E6/Ktt))
    ax.legend(prop={'size': 8})   

    
def hardening_TSL(C_0, Ktt, H, ratio):
    C_u=C_0*((H/Ktt)*(ratio-1)+1)**0.5
    DV_u=((C_u-C_0)/H + C_0/Ktt)*1000
    DV1=np.linspace(0,C_0*1000/Ktt,10)
    DV2=np.linspace(C_0*1000/Ktt,DV_u,11)
    DV2=np.delete(DV2,0)
    DV=np.append(DV1, DV2)
    tau1=np.linspace(0,C_0,10)
    tau2=np.linspace(C_0,C_u,11)
    tau2=np.delete(tau2, 0)
    tau=np.append(tau1,tau2)
    return DV, DV1, tau, tau1, C_u

def hardening_TSL_ploter(fig, ax, C_0, Ktt, H, ratio, hatch='false'):
    DV,DV1,tau,tau1,C_u = hardening_TSL(C_0, Ktt, H, ratio)
    ax.plot(DV, tau, label='C0={} MPa, Cu={} MPa, Ktt={} MN/m3, H={} MN/m3, Gf/Go = {}'.format(C_0, C_u, 
        int(Ktt) if float(Ktt).is_integer() else "{:.2f}".format(Ktt), H, ratio))
    if hatch =='true':
        ax.fill_between(DV1, tau1, alpha=0.05 , label='G_o={} N/m (J/m^2)'.format(C_0*C_0*1E6/Ktt))
    ax.legend(prop={'size': 8})   

def threshold_surface(c, ft, phi, max_c=0):
    # max_c is defined to make a fixed left side domain's limit for threshold_surface plots
    # when you want to use this function in a loop to draw different threshold_surface in one curve
    if max_c == 0:
        max_c=c
    sigma_ell=np.linspace(0,ft,100)
    sigma_c=-phi*ft**2/(c-2*ft*phi)  # see atena theory manual
    tau0=c/(1-(sigma_c**2/(ft-sigma_c)**2))**0.5 # see atena theory manual
    tau_ell=tau0*(1-((sigma_ell-sigma_c)/(ft-sigma_c))**2)**0.5
    sigma_lin=np.linspace(0,-max_c,10)
    sigma_lin=np.delete(sigma_lin,0)
    tau_lin=c-sigma_lin*phi
    sigma=np.append(sigma_lin,sigma_ell)
    tau=np.append(tau_lin,tau_ell)
    return sigma, tau

def threshold_ploter(fig, ax, c, ft, phi, max_c=[]):
    sigma, tau  = threshold_surface(c, ft, phi, max_c)
    ax.plot(sigma, tau, color='b', linewidth=0.8)
    #path_ploter(ax, ft, c)

def path_ploter(ax, x, y):
    u = np.diff(x)
    v = np.diff(y)
    pos_x = x[:-1] + u/2
    pos_y = y[:-1] + v/2
    norm = np.sqrt(u**2+v**2)    
    ax.plot(x,y, marker="o",markersize=4)
    ax.quiver(pos_x, pos_y, u/norm, v/norm, angles='xy', zorder=5, pivot="mid")
    return ax
    

def figs(axins_dim=[0.08, 0.72, 0.2, 0.2]):
    fig1, ax1 = plt.subplots()
    fig1.suptitle('Interface Traction Separation Law')
    ax1.set(xlabel='Dv (sliding) (mm)', ylabel='Shear Stress (MPa)')
    ax1.grid(color='k', linewidth=0.1)
    plt.rcParams.update({'font.size': 5})
    axins = ax1.inset_axes(axins_dim)
    axins.set(xlabel='Normal stress (MPa)', ylabel='Tangential stress (MPa)')
    axins.grid(color='k', linewidth=0.1)
    axins.axis('equal')
    axins.set_title('Threshold surface') 
    plt.rcParams.update({'font.size': 10})
    return fig1, ax1, axins
        
def PS1():
    ratio=2
    C_0= np.array([1,2,3])
    ft_0=C_0
    Ktt=5000
    phi=0.3
    fig1, ax1, axins = figs()
    for i, value in enumerate(C_0):
        c , ft = C_0[i], ft_0[i]
        bilin_TSL_ploter(fig1, ax1, c, Ktt, ratio, hatch='true')
        threshold_ploter(fig1, axins, c, ft, phi, max(C_0))


def PS2():
    ratio=2
    C_0= 1 
    c=C_0
    ft=C_0
    phi=0.3
    Ktt=[5000,5000/2,5000/3]
    fig1, ax1, axins = figs(axins_dim=[0.82, 0.5, 0.15, 0.15])
    for i, value in enumerate(Ktt):
        bilin_TSL_ploter(fig1, ax1, c, value, ratio, hatch='true')
        threshold_ploter(fig1, axins, c, ft, phi, c)
        
    

def PS3():
    ratio=2
    phi=0.3
    C_0_min= 1 
    C_0_Max= 3
    Ktt=5000
    r=np.linspace(1,C_0_Max/C_0_min,3)
    C_0=r*C_0_min
    Ktt=r*Ktt
    fig1, ax1, axins = figs()
    for i, value in enumerate(r):
        c, ktt = C_0[i], Ktt[i]
        ft = c
        bilin_TSL_ploter(fig1, ax1, c, ktt, ratio, hatch='true')
        threshold_ploter(fig1, axins, c, ft, phi, max(C_0))

def PS4():
    ratio=[1, 1.5 ,2, 3]
    C_0 = 2 
    ft=C_0
    ktt=5000
    H = 2000
    phi=0.3
    fig1, ax1, axins = figs(axins_dim=[0.08, 0.45, 0.15, 0.15])
    for i, value in enumerate(ratio):
            bilin_TSL_ploter(fig1, ax1, C_0, ktt, value)
    plateau_TSL_ploter(fig1, ax1, C_0, ktt, 2*ratio[-1]-1)
    hardening_TSL_ploter(fig1, ax1, C_0, ktt, H, H/ktt*(ratio[-1]-1)**2+(2*ratio[-1]-1), hatch='true')
    threshold_ploter(fig1, axins, C_0, ft, phi,C_0)

PS1() 
PS2() 
PS3() 
PS4() 

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
