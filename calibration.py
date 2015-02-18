import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import LinearLocator, FormatStrFormatter

from matplotlib import cm
import numpy as np
from scipy.optimize import minimize
import scipy
from mpl_toolkits.mplot3d import Axes3D

matplotlib.pyplot.close('all')

entryoffsets = pd.read_csv("entryoffsets.csv")
winratios = pd.read_csv("winratios.csv")
volmeans = pd.read_csv("vols.csv")

data = pd.DataFrame(columns=['weights','entryoffsets','vol','winratio'])

data['winratio']=winratios.stack().values
data['entryoffsets']=entryoffsets.stack().values
data['vol']=pd.DataFrame(map(lambda x: np.repeat(x,7),volmeans['0'])).stack().values
data['weights']=np.repeat(1,len(data['vol']))


def calib_func(x,vol,trend,wins):
    a1=(x[0]*vol+x[1]*vol+x[2])/(1+np.exp(x[3]*trend/vol))
    b1=(0.5-(x[0]*vol**0.5+x[1]*vol+x[2])/2.0)
    return (np.mean(((a1+b1 - wins))**2))**0.5

def price(vol,trend):
    a1=(x[0]*vol+x[1]*vol+x[2])/(1+np.exp(x[3]*trend/vol))
    b1=(0.5-(x[0]*vol**0.5+x[1]*vol+x[2])/2.0)
    return a1+b1

guess = (0.1,0.1,0.1,0.1)
p1=scipy.optimize.minimize(calib_func,guess,args=(data['vol'],data['entryoffsets']/data['vol'],data['winratio'],),method='Nelder-Mead',options={'gtol': 1e-11,'disp':True})
x=p1.x
print p1

X=data['entryoffsets']/data['vol']
Y=data['vol']
X,Y= np.meshgrid(X,Y)
Z =  map(price,Y,X)
fig = plt.figure()
ax = fig.gca(projection='3d')
fig.set_size_inches(12.5,7.5)
surf = ax.plot_surface(X, Y*1e3, Z, rstride=1, cstride=1, cmap=cm.hot_r,linewidth=0, antialiased=True)
ax.zaxis.set_major_locator(LinearLocator(10))
ax.zaxis.set_major_formatter(FormatStrFormatter('%.2f'))
fig.colorbar(surf, shrink=0.5, aspect=10)
plt.show()


                              
