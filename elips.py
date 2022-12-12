import numpy as np
import matplotlib.pylab as plt

# source: atena theory manual
phi=0.3
ft=3
c=3
sigma_ell=np.linspace(0,ft,100)
sigma_c=-phi*ft**2/(c-2*ft*phi)
tau0=c/(1-(sigma_c**2/(ft-sigma_c)**2))**0.5
tau_ell=tau0*(1-((sigma_ell-sigma_c)/(ft-sigma_c))**2)**0.5

sigma_lin=np.linspace(0,-3*ft,10)
sigma_lin=np.delete(sigma_lin,0)
tau_lin=c-sigma_lin*phi

sigma=np.append(sigma_lin,sigma_ell)
tau=np.append(tau_lin,tau_ell)
fig, ax = plt.subplots()
fig.suptitle('Threshold surface')
ax.set(xlabel='Normal stress (MPa)', ylabel='Tangential stress (MPa)')
ax.plot(sigma,tau, color='b',linewidth=0.8)
ax.axvline(x=0 , linestyle='dashed', color='k', linewidth=0.5)
ax.axhline(y=0 , linestyle='dashed', color='k', linewidth=0.5)
plt.show()



# below. source: Coupled sliding-decohesion-compression model for a consistent description of monotonic and fatigue behavior of material interfaces
""" xb=4
yb=4
x0=0
y0=0
m=0.3

xc= m*(xb**2-2*xb*x0+x0**2)/(2*m*xb-2*m*x0-yb)
c=m*(xb**2-2*xb*x0+x0**2)/(2*m*xb-2*m*x0-yb)
b=((yb**0.5)*(-m*xb+m*x0+yb)*(1/(-2*m*xb+2*m*x0+yb))**0.5)/c
a=-((xb-x0)*(-m*xb+m*x0+yb))/(c*(-2*m*xb+2*m*x0+yb))
x_ell=np.linspace(0,xb,100)
x_lin=np.linspace(0,-3*xb,10)
x=np.append(x_ell,x_lin)
y_ell=-b*(c**2-((x_ell-x0-xc)**2)/a**2)**0.5
y_lin=yb-x_lin*m
y=np.append(y_ell,y_lin)
fig, ax = plt.subplots()
fig.suptitle('Threshold surface')
ax.set(xlabel='Normal stress (MPa)', ylabel='Tangential stress (MPa)')
ax.plot(x_lin,y_lin, color='b',linewidth=0.8)
ax.plot(x_ell,y_ell, color='b',linewidth=0.8)
ax.axvline(x=0 , linestyle='dashed', color='k', linewidth=0.5)
plt.show() """