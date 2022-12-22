import matplotlib.pyplot as plt
import numpy as np
from collections import OrderedDict
from matplotlib.ticker import  (MultipleLocator, AutoMinorLocator, FormatStrFormatter)


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

def bilin_TSL_ploter(fig, ax, C_0, Ktt, ratio, hatch ='false', legend='off'):
    DV,DV1,tau,tau1 = biliner_TSL(C_0,Ktt,ratio)
    ax.plot(DV, tau, label='C0={} MPa , Ktt={} MN/m3, Gf/Go = {}'.format(C_0, 
        int(Ktt) if float(Ktt).is_integer() else "{:.2f}".format(Ktt), ratio))
    if hatch =='true':
        ax.fill_between(DV1, tau1, alpha=0.25 , label='G_o={} N/m (J/m^2)'.format(C_0*C_0*1E6/Ktt))
    if legend=='on':
        box = ax.get_position()
        ax.set_position([box.x0, box.y0 + box.height * 0.05,
                    box.width, box.height * 0.95])
        ax.legend(prop={'size': 6}, loc='upper center', bbox_to_anchor=(0.5, -0.15),
            fancybox=True, shadow=True, ncol=2, borderaxespad=0)          
    
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

def plateau_TSL_ploter(fig, ax, C_0, Ktt, ratio, hatch='false', legend='off'):
    DV,DV1,tau,tau1 = plateau_TSL(C_0,Ktt,ratio)
    ax.plot(DV, tau, label='C0={} MPa , Ktt={} MN/m3, Gf/Go = {}'.format(C_0, 
        int(Ktt) if float(Ktt).is_integer() else "{:.2f}".format(Ktt), ratio))
    if hatch =='true':
        ax.fill_between(DV1, tau1, alpha=0.25 , label='G_o={} N/m (J/m^2)'.format(C_0*C_0*1E6/Ktt))
    if legend=='on':
        box = ax.get_position()
        ax.set_position([box.x0, box.y0 + box.height * 0.05,
                    box.width, box.height * 0.95])
        ax.legend(prop={'size': 6}, loc='upper center', bbox_to_anchor=(0.5, -0.25),
            fancybox=True, shadow=True, ncol=2)          
    
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

def hardening_TSL_ploter(fig, ax, C_0, Ktt, H, ratio, hatch='false', legend='off'):
    DV,DV1,tau,tau1,C_u = hardening_TSL(C_0, Ktt, H, ratio)
    ax.plot(DV, tau, label='C0={} MPa, Cu={} MPa, Ktt={} MN/m3, \n H={} MN/m3, Gf/Go = {}'.format(C_0, C_u, 
        int(Ktt) if float(Ktt).is_integer() else "{:.2f}".format(Ktt), H, ratio))
    if hatch =='true':
        ax.fill_between(DV1, tau1, alpha=0.25 , label='G_o={} N/m (J/m^2)'.format(C_0*C_0*1E6/Ktt))
    if legend=='on':
        box = ax.get_position()
        ax.set_position([box.x0, box.y0 + box.height * 0.05,
                    box.width, box.height * 0.95])
        ax.legend(prop={'size': 6}, loc='upper center', bbox_to_anchor=(0.5, -0.15),
            fancybox=True, shadow=True, ncol=2)         
    
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
    
def path_ploter(ax, x, y):
    u = np.diff(x)
    v = np.diff(y)
    pos_x = x[:-1] + u/2
    pos_y = y[:-1] + v/2
    norm = np.sqrt(u**2+v**2)    
    ax.plot(x,y, marker="o",markersize=2,linewidth=0.6)
    linestyles = OrderedDict([
        ('loosely dashed',      (0, (3, 6))),
        ('dashed',              (0, (10, 4))),
        ('densely dashed',      (0, (1, 3))),])
    ax.vlines(x, 0, y, linewidth=0.6 , linestyles=linestyles['loosely dashed'])
    ax.hlines(y, 0, x, linewidth=0.6 , linestyles=linestyles['loosely dashed'])
    ax.quiver(pos_x, pos_y, u/norm, v/norm, angles='xy', zorder=5, pivot="mid")
    return ax 

def N_TSL(F_t,Knn,N_ratio):
    DU1=np.linspace(0,F_t*1000/Knn,10)
    DU2=np.linspace(F_t*1000/Knn,(N_ratio)*F_t*1000/Knn,11)
    DU2=np.delete(DU2,0)
    DU=np.append(DU1,DU2)
    sigma1=np.linspace(0,F_t,10)
    sigma2=np.linspace(F_t,0,11)
    sigma2=np.delete(sigma2,0)
    sigma=np.append(sigma1, sigma2)
    return DU, sigma

def N_TSL_ploter(ax, F_t, Knn, N_ratio, legend='off'):
    DU, sigma = N_TSL(F_t, Knn, N_ratio)
    ax.plot(DU, sigma, label='F_t={} MPa, Knn={} MN/m3, ratio={}'.format(F_t,
        int(Knn) if float(Knn).is_integer() else '{:.2f}'.format(Knn), N_ratio))
    if legend=='on':
        ax.legend(prop={'size': 8})   
    
def figs(axins_dim1=[0.06, 0.79, 0.18, 0.18],axins_dim2=[0.06, 0.52, 0.18, 0.18]):
    ax_fontsize , axin_fontsize = 8, 5
    plt.rcParams.update({'font.size': ax_fontsize})
    fig1, ax1 = plt.subplots()
    #fig1.suptitle('Interface Traction Separation Law')
    ax1.set(xlabel='Dv (sliding (mm)) ', ylabel='Shear Stress (MPa)')
    #ax1.grid(color='k', linewidth=0.1)
    plt.rcParams.update({'font.size': axin_fontsize})
    axins1 = ax1.inset_axes(axins_dim1)
    axins1.set_xlabel(xlabel='Normal stress (MPa)', labelpad=0)
    axins1.set_ylabel(ylabel='Tangential stress (MPa)', labelpad=0)
    axins1.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
    #axins1.set_ymargin(0)
    #axins1.grid(color='k', linewidth=0.1)
    #axins1.axis('equal')
    #axins1.set_title('Threshold surface') 
    axins2 = ax1.inset_axes(axins_dim2)
    axins2.set_xlabel(xlabel='Du (Opening (mm))', labelpad=0)
    axins2.set_ylabel(ylabel='Normal Stress (MPa)' , labelpad=0 )
    axins1.xaxis.set_major_locator(MultipleLocator(1))
    axins1.yaxis.set_major_locator(MultipleLocator(1))
    axins2.xaxis.set_major_locator(MultipleLocator(0.2))
    axins2.yaxis.set_major_locator(MultipleLocator(0.5))
    plt.rcParams.update({'font.size': ax_fontsize})
    return fig1, ax1, axins1, axins2

def savefig_nomargin(name):
    plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, 
                 hspace = 0, wspace = 0)
    plt.margins(0,0)
    plt.savefig("{}.pdf".format(name), bbox_inches = 'tight' , pad_inches = 0)   
    plt.tight_layout()

    
    
def PS1():
    ratio=2
    C_0= np.array([1,2,3])
    ft_0=np.array([C_0[0],C_0[0],C_0[0]])
    Ktt=5000
    phi=0.3#
    Knn=5000
    N_ratio=2
    fig1, ax1, axins1, axins2 = figs()
    for i, value in enumerate(C_0):
        c , ft = C_0[i], ft_0[i]
        bilin_TSL_ploter(fig1, ax1, c, Ktt, ratio, hatch='false', legend='off')
        threshold_ploter(fig1, axins1, c, ft, phi, max(C_0))
    path_ploter(axins1, ft_0, C_0)
    N_TSL_ploter(axins2, ft_0[0], Knn, N_ratio)
    savefig_nomargin('PS1')


def PS2():
    ratio=2
    C_0= 1 
    c=C_0
    ft=C_0
    phi=0.3
    Ktt=[5000,5000/2,5000/3]
    Knn=5000
    N_ratio=2
    fig1, ax1, axins1, axins2  = figs(axins_dim1=[0.8, 0.79, 0.18, 0.18],axins_dim2=[0.8, 0.52, 0.18, 0.18])
    for i, value in enumerate(Ktt):
        bilin_TSL_ploter(fig1, ax1, c, value, ratio, hatch='false', legend='off')
        threshold_ploter(fig1, axins1, c, ft, phi, c)
    N_TSL_ploter(axins2, ft, Knn, N_ratio)
    savefig_nomargin('PS2')

    

def PS3():
    ratio=2
    phi=0.3
    C_0_min= 1 
    C_0_Max= 3
    Ktt=5000
    r=np.linspace(1,C_0_Max/C_0_min,3)
    C_0=r*C_0_min
    ft_0=np.array([C_0[0],C_0[0],C_0[0]])
    Ktt=r*Ktt
    Knn=5000
    N_ratio=2
    fig1, ax1, axins1, axins2  = figs()
    for i, value in enumerate(r):
        c, ktt,ft = C_0[i], Ktt[i], ft_0[i]
        bilin_TSL_ploter(fig1, ax1, c, ktt, ratio, hatch='false', legend='off')
        threshold_ploter(fig1, axins1, c, ft, phi, max(C_0))
    path_ploter(axins1, ft_0, C_0)
    N_TSL_ploter(axins2, ft_0[0], Knn, N_ratio)
    savefig_nomargin('PS3')

    
def PS4():
    ratio=[1, 1.5 ,2, 3]
    C_0 = 2 
    ft=C_0
    ktt=5000
    H = 2000
    phi=0.3
    Knn=5000
    N_ratio=2
    fig1, ax1, axins1, axins2  = figs()
    for i, value in enumerate(ratio):
            bilin_TSL_ploter(fig1, ax1, C_0, ktt, value)
    plateau_TSL_ploter(fig1, ax1, C_0, ktt, 2*ratio[-1]-1)
    hardening_TSL_ploter(fig1, ax1, C_0, ktt, H, H/ktt*(ratio[-1]-1)**2+(2*ratio[-1]-1), hatch='false', legend='off')
    threshold_ploter(fig1, axins1, C_0, ft, phi,C_0)
    N_TSL_ploter(axins2, ft, Knn, N_ratio)
    savefig_nomargin('PS4')
 

PS1() 
PS2() 
PS3() 
PS4() 





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