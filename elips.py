import sympy as sp
import numpy as np
import matplotlib.pylab as plt
from mpl_toolkits.mplot3d import Axes3D
sp.init_printing()
from cymbol import Cymbol, ccode

x, y = sp.symbols('x, y')

x_c = sp.symbols('x_c')  # center point of an ellipse
a = sp.symbols('a', nonnegative=True)
b = sp.symbols('b', nonnegative=True)
c = sp.symbols('c', positive=True)

x_0 = sp.symbols('x_0')
x_bar, y_bar = sp.symbols(r'\bar{x}, \bar{y}', nonnegative=True )
f_mid_ = sp.sqrt(y**2) - (y_bar - m * (x-x_0))
