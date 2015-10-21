# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 18:48:06 2015

@author: hossein
"""
import re
import numpy as np

import matplotlib.pyplot as plt
import matplotlib
import mpl_toolkits.mplot3d as a3
from matplotlib.ticker import LinearLocator, FormatStrFormatter


def read_in_grid(filename):
    grid_file=open(filename,'r')
    line=grid_file.readline()
    X=re.findall(r"[+-]? *(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?", line)
    line=grid_file.readline()
    Y=re.findall(r"[+-]? *(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?", line)
    size_x=int(X[0])
    size_y=int(Y[0])
    XYZ= np.zeros((size_x,size_y,3))
    range_x=[float(X[1]),float(X[2])]
    range_y=[float(Y[1]),float(Y[2])]
    dx=(range_x[1]-range_x[0])/size_x
    dy=(range_y[1]-range_y[0])/size_y
    xvec=np.linspace(range_x[0]+.5*dx,range_x[1]-.5*dx,size_x)
    yvec=np.linspace(range_y[0]+.5*dy,range_y[1]-.5*dy,size_y)
    XYZ[:,:,0],XYZ[:,:,1]=np.meshgrid(xvec, yvec, sparse=False, indexing='ij')
#    xmesh=np.reshape(((2*np.arange(size_x)+0.5)/(2*size_x)*
#		(range_x[1]-range_x[0])+range_x[0]),(1,size_x))
#    ymesh=np.reshape(((2*np.arange(size_y)+0.5)/(2*size_y)*
#    (range_y[1]-range_y[0])+range_y[0]),(1,size_y))
#    XYZ[:,:,0]=xmesh.T*np.matrix(np.ones((1,size_y)))
#    XYZ[:,:,1]=np.matrix(np.ones((1,size_x))).T*ymesh

    line=grid_file.readline()
    for i in range(size_y):
        line=grid_file.readline()
        XYZ[:,i,2] = [float(x) for x in line.split()]
        
    grid_file.close()
    return XYZ



xyh=read_in_grid('pileheightrecord.-00001')	
dxdy=[(xyh[1,0,0]-xyh[0,0,0]),(xyh[0,1,1]-xyh[0,0,1])]
dxdy_a=dxdy[0]*dxdy[1]
vol=np.sum(xyh[:,:,2]*dxdy_a)
h=xyh[:,:,2]
xyh=[]
maxh=np.max(h)
XYZ=read_in_grid('elevation.grid');

cmap=matplotlib.cm.jet
norm = matplotlib.colors.Normalize(vmin=-4, vmax=np.log10(np.max(h[:,:])))
m = matplotlib.cm.ScalarMappable(norm=norm, cmap=cmap)
h[h<1e-4]=1e-4

rang=m.to_rgba(np.log10(h))
Nx=len(XYZ[:,0,0])
Ny=len(XYZ[0,:,0])
for i in range(Nx):
    for j in range (Ny):
        if np.array_equal(rang[i,j,:],[0,0,.5,1]):
            rang[i,j,:]=[1,1,1,1]
            
fig = plt.figure(frameon=False)
ax = fig.gca(projection='3d')
surf = ax.plot_surface(XYZ[:,:,0], XYZ[:,:,1], XYZ[:,:,2], rstride=1, cstride=1,
                       facecolors=rang,
                       linewidth=0, antialiased=False)

#ax.zaxis.set_major_locator(LinearLocator(5))
#ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

ax.view_init(elev=0,azim=0)
ax.axis('off')
#fig.colorbar(surf, shrink=0.5, aspect=5)
plt.savefig('foo.png')
plt.show()

