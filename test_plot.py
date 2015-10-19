# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 18:48:06 2015

@author: hossein
"""
import re
import numpy as np

import matplotlib.pyplot as plt
import matplotlib
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection

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
	
	xmesh=np.reshape(((2*np.arange(size_x)+0.5)/(2*size_x)*
		(range_x[1]-range_x[0])+range_x[0]),(1,size_x))
		
	ymesh=np.reshape(((2*np.arange(size_y)+0.5)/(2*size_y)*
		(range_y[1]-range_y[0])+range_y[0]),(1,size_y))	
		
	XYZ[:,:,0]=xmesh.T*np.matrix(np.ones((1,size_y)))
	XYZ[:,:,1]=np.matrix(np.ones((1,size_x))).T*ymesh
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
X=XYZ[:,:,0]
Y=XYZ[:,:,1]
Z=XYZ[:,:,2]
XYZ=[]
xminmax=[np.min(X[:,0]),np.max(X[:,0])]
yminmax=[np.min(Y[0,:]),np.max(Y[0,:])]
Nx=len(X[:,0])
Ny=len(Y[0,:])
Nquads=(Nx-1)*(Ny-1)
quads=np.zeros((4,Nx-1,Ny-1))
patches = []
fig, ax = plt.subplots()
cmap=matplotlib.cm.jet
#a=np.floor(np.log10(np.min(h[:,:])))
b=np.ceil(np.log10(np.max(h[:,:])))
#b=max(h[:,:])
minmaxh=np.power(10,[-2,b])
#norm = matplotlib.colors.Normalize(vmin=minmaxh[0], vmax=minmaxh[1])
norm = matplotlib.colors.Normalize(vmin=np.min(h[:,:]), vmax=np.max(h[:,:]))
m = matplotlib.cm.ScalarMappable(norm=norm, cmap=cmap)
 
for i in range(Nx-1):
	for j in range(Ny-1):
         x1=X[i,j]
         x2=X[i+1,j]
         y1=Y[i,j]
         y2=Y[i,j+1]
         points=[[x1,y1],[x2,y1],[x2,y2],[x1,y2]]
#         if h[i,j]==0:
#             h[i,j]=.01             
         polygon = plt.Polygon(points,facecolor=m.to_rgba(h[i,j]))
         patches.append(polygon)
         
#p = PatchCollection(patches, cmap=matplotlib.cm.jet, alpha=0.4)
p = PatchCollection(patches,match_original=True)         
print len(patches)
colors = [0,1,2,1]
#100*np.random.rand(len(patches))
#p.set_array(np.array(colors))

ax.add_collection(p)
ax.relim()
ax.set_xlim([xminmax[0], xminmax[1]])
ax.set_ylim([yminmax[0], yminmax[1]])
plt.show()    
	

#Polygon
#fig, ax = plt.subplots()
#patches = []
#
#for i in range(Nx-1):
#	for j in range(Ny-1):
#         polygon = Polygon([X[i,j],X[i+1,j],Y[i,j],Y[i,j+1]], True)
#         patches.append(polygon)
#
#p = PatchCollection(patches, cmap=matplotlib.cm.jet, alpha=0.4)
#
#colors = 100*np.random.rand(len(patches))
#p.set_array(np.array(colors))
#
#ax.add_collection(p)
#
#plt.show()
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
#quads[0,:,:]=
#quads[1,:,:]=
#quads[2,:,:]=
#quads[3,:,:]=