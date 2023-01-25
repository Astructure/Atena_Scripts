import matplotlib.pyplot as plt
import numpy as np
import os
from collections import OrderedDict
from matplotlib.ticker import  (MultipleLocator, AutoMinorLocator, FormatStrFormatter)

# function block related to interface material model (CZM) 

def biliner_TSL(C_0,Ktt,ratio):
    # ratio = G_f/G_o #bilnear CZL
    DV1=np.linspace(0,C_0/Ktt,10)
    DV2=np.linspace(C_0/Ktt,(ratio)*C_0/Ktt,11)
    DV2=np.delete(DV2,0)
    DV=np.append(DV1, DV2)
    tau1=np.linspace(0,C_0,10)
    tau2=np.linspace(C_0,0,11)
    tau2=np.delete(tau2, 0)
    tau=np.append(tau1,tau2)
    return DV, DV1, tau, tau1

def bilin_TSL_ploter(fig, ax, C_0, Ktt, ratio, hatch ='false', legend='off', linewidth=1.5):
    DV,DV1,tau,tau1 = biliner_TSL(C_0,Ktt,ratio)
    Dv_f, C_Dv_f = DV[-1], tau[-1]
    ax.plot(DV*1000, tau, label='C0={} MPa , Ktt={} MN/m3, Gf/Go = {}'.format(C_0, 
        int(Ktt) if float(Ktt).is_integer() else "{:.2f}".format(Ktt), ratio), linewidth=linewidth)
    if hatch =='true':
        ax.fill_between(DV1, tau1, alpha=0.25 , label='G_o={} N/m (J/m^2)'.format(C_0*C_0*1E6/Ktt))
    if legend=='on':
        box = ax.get_position()
        ax.set_position([box.x0, box.y0 + box.height * 0.05,
                    box.width, box.height * 0.95])
        ax.legend(prop={'size': 10}, loc='upper center', bbox_to_anchor=(0.5, -0.15),
            fancybox=True, shadow=True, ncol=2, borderaxespad=0)   
    return Dv_f, C_Dv_f

def plateau_TSL(C_0,Ktt,ratio):
    # ratio = G_f/G_o #plateau CZL
    DV1=np.linspace(0,C_0/Ktt,10)
    DV2=np.linspace(C_0/Ktt,0.5*(ratio+1)*C_0/Ktt,11)
    DV2=np.delete(DV2,0)
    DV=np.append(DV1, DV2)
    tau1=np.linspace(0,C_0,10)
    tau2=np.linspace(C_0,C_0,11)
    tau2=np.delete(tau2, 0)
    tau=np.append(tau1,tau2)
    return DV, DV1, tau, tau1

def plateau_TSL_ploter(fig, ax, C_0, Ktt, ratio, hatch='false', legend='off'):
    DV,DV1,tau,tau1 = plateau_TSL(C_0,Ktt,ratio)
    Dv_f, C_Dv_f = DV[-1], tau[-1]/C_0
    ax.plot(DV*1000, tau, label='C0={} MPa , Ktt={} MN/m3, Gf/Go = {}'.format(C_0, 
        int(Ktt) if float(Ktt).is_integer() else "{:.2f}".format(Ktt), ratio))
    if hatch =='true':
        ax.fill_between(DV1, tau1, alpha=0.25 , label='G_o={} N/m (J/m^2)'.format(C_0*C_0*1E6/Ktt))
    if legend=='on':
        box = ax.get_position()
        ax.set_position([box.x0, box.y0 + box.height * 0.05,
                    box.width, box.height * 0.95])
        ax.legend(prop={'size': 10}, loc='upper center', bbox_to_anchor=(0.5, -0.25),
            fancybox=True, shadow=True, ncol=2)          
    return Dv_f, C_Dv_f
    
def hardening_TSL(C_0, Ktt, H, ratio):
    C_u=C_0*((H/Ktt)*(ratio-1)+1)**0.5
    DV_u=((C_u-C_0)/H + C_0/Ktt)
    DV1=np.linspace(0,C_0/Ktt,10)
    DV2=np.linspace(C_0/Ktt,DV_u,11)
    DV2=np.delete(DV2,0)
    DV=np.append(DV1, DV2)
    tau1=np.linspace(0,C_0,10)
    tau2=np.linspace(C_0,C_u,11)
    tau2=np.delete(tau2, 0)
    tau=np.append(tau1,tau2)
    return DV, DV1, tau, tau1, C_u

def hardening_TSL_ploter(fig, ax, C_0, Ktt, H, ratio, hatch='false', legend='off'):
    DV,DV1,tau,tau1,C_u = hardening_TSL(C_0, Ktt, H, ratio)
    Dv_f, C_Dv_f = DV[-1], tau[-1]/C_0
    ax.plot(DV*1000, tau, label='C0={} MPa, Cu={} MPa, Ktt={} MN/m3, \n H={} MN/m3, Gf/Go = {}'.format(C_0, C_u, 
        int(Ktt) if float(Ktt).is_integer() else "{:.2f}".format(Ktt), H, ratio))
    if hatch =='true':
        ax.fill_between(DV1, tau1, alpha=0.25 , label='G_o={} N/m (J/m^2)'.format(C_0*C_0*1E6/Ktt))
    if legend=='on':
        box = ax.get_position()
        ax.set_position([box.x0, box.y0 + box.height * 0.05,
                    box.width, box.height * 0.95])
        ax.legend(prop={'size': 10}, loc='upper center', bbox_to_anchor=(0.5, -0.15),
            fancybox=True, shadow=True, ncol=2)         
    return Dv_f, C_Dv_f
     
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

def threshold_ploter(fig, ax, c, ft, phi, max_c=[]):
    sigma, tau  = threshold_surface(c, ft, phi, max_c)
    ax.plot(sigma, tau, color='b', linewidth=0.8)  

def N_TSL(F_t,Knn,N_ratio):
    DU1=np.linspace(0,F_t/Knn,10)
    DU2=np.linspace(F_t/Knn,(N_ratio)*F_t/Knn,11)
    DU2=np.delete(DU2,0)
    DU=np.append(DU1,DU2)
    sigma1=np.linspace(0,F_t,10)
    sigma2=np.linspace(F_t,0,11)
    sigma2=np.delete(sigma2,0)
    sigma=np.append(sigma1, sigma2)
    return DU, sigma

def N_TSL_ploter(ax, F_t, Knn, N_ratio, legend='off'):
    DU, sigma = N_TSL(F_t, Knn, N_ratio)
    Du_f, Ft_Du_f =  DU[-1], sigma[-1]
    ax.plot(DU*1000, sigma, label='F_t={} MPa, Knn={} MN/m3, ratio={}'.format(F_t,
        int(Knn) if float(Knn).is_integer() else '{:.2f}'.format(Knn), N_ratio))
    if legend=='on':
        ax.legend(prop={'size': 10})   
    return Du_f, Ft_Du_f
    
    # figs(axins_dim1=[0.08, 0.80, 0.16, 0.16],axins_dim2=[0.08, 0.54, 0.16, 0.16])
    # figs(axins_dim2=[0.3, 0.1, 0.16, 0.16],axins_dim1=[0.6, 0.1, 0.16, 0.16])
def figs(axins_dim1=[0.08, 0.80, 0.16, 0.16],axins_dim2=[0.08, 0.54, 0.16, 0.16]):
    ax_fontsize , axin_fontsize = 16, 9
    plt.rcParams.update({'font.size': ax_fontsize})
    fig1, ax1 = plt.subplots(figsize=(5.5, 4.5))
    #fig1.suptitle('Interface Traction Separation Law')
    ax1.set(xlabel='Dv (sliding (mm)) ', ylabel='Shear Stress (MPa)')
    #ax1.grid(color='k', linewidth=0.1)
    plt.rcParams.update({'font.size': axin_fontsize})
    axins1 = ax1.inset_axes(axins_dim1)
    axins1.set_xlabel(xlabel='Normal stress', labelpad=0)
    axins1.set_ylabel(ylabel='Tangential stress', labelpad=0)
    axins1.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
    #axins1.set_ymargin(0)
    #axins1.grid(color='k', linewidth=0.1)
    #axins1.axis('equal')
    #axins1.set_title('Threshold surface') 
    axins2 = ax1.inset_axes(axins_dim2)
    axins2.set_xlabel(xlabel='Du (Opening)', labelpad=0)
    axins2.set_ylabel(ylabel='Normal Stress' , labelpad=0 )
    axins1.xaxis.set_major_locator(MultipleLocator(1))
    axins1.yaxis.set_major_locator(MultipleLocator(1))
    axins2.xaxis.set_major_locator(MultipleLocator(0.4))
    axins2.yaxis.set_major_locator(MultipleLocator(0.5))
    plt.rcParams.update({'font.size': ax_fontsize})
    return fig1, ax1, axins1, axins2


def savefig_nomargin(output_dir, name):
    plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, 
                 hspace = 0.15, wspace = 0)
    plt.margins(0,0)
    my_file = "{}.pdf".format(name)
    plt.savefig(os.path.join(output_dir, my_file), bbox_inches = 'tight' , pad_inches = 0)   
    plt.tight_layout()

# function block related to FRP Yarn material model

def frp_yarn_plotter(ax, Ft=3.3, E=230, nu=0.3):
    ax.set(xlabel='strain (%)', ylabel='Stress (GPa)')
    strain=np.linspace(0,Ft/E,10)*100
    Stress=np.linspace(0,Ft,10)
    ax.plot(strain, Stress)
    xmax = strain.max()
    ymax = Stress.max()
    X_extraticks=[xmax]
    Y_extraticks=[ymax]
    secax_x = ax.secondary_xaxis('top')
    secax_x.set_xticks(X_extraticks)
    secax_y = ax.secondary_yaxis('right')
    secax_y.set_yticks(Y_extraticks)
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    ax.text(0.05, 0.95, 'E={} GPa ; v={}'.format(E, nu), transform=ax.transAxes, fontsize=10,
            verticalalignment='top', bbox=props)
