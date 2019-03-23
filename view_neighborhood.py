# Tools for looking at small regions of 3d simulation
# And diagnosing small timestep 

import reader as cr
import numpy as n

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib.colors as mco

def view(data,log=True):
    # Makes scatterplot out of 3-D array
    fig = plt.figure()
    ax = fig.add_subplot(111,projection='3d',axisbg='k')
    x1,x2,x3 = n.indices(data.shape)
    if log:
        lnorm = mco.LogNorm()
    else:
        lnorm = None
    axs = ax.scatter(x1.flatten(),x2.flatten(),x3.flatten(),c=data.flatten(),edgecolors='none',norm=lnorm,cmap='viridis',alpha=1,lw=0)
    fig.colorbar(axs)
    plt.show()

def view4(datas):
    # takes in 4 arrays (density and 3 velocity), showing velocity direction 
    x1,x2,x3 = n.indices(datas[0].shape)
    x1f = x1.flatten()
    x2f = x2.flatten()
    x3f = x3.flatten()
    i0 = len(x1f)/2
    x1f0 = x1f[i0]
    x2f0 = x2f[i0]
    x3f0 = x3f[i0]
    sizes = n.zeros(len(x1f)) + 25
    sizes[i0] += 36
    fig = plt.figure()
    ax = range(4)
    axs = range(4)
    norms = [mco.LogNorm(),None,None,None]
    cmaps = ['viridis','seismic','seismic','seismic']
    for i in range(4):
        df = datas[i].flatten()
        ax[i] = fig.add_subplot(2,2,i+1,projection='3d',axisbg='k')
        axs[i] = ax[i].scatter(x1f,x2f,x3f,s=sizes,c=df,edgecolors='none',norm=norms[i],cmap=cmaps[i],alpha=1,lw=0)
        ql = 1.0
        qd = n.sign(df[i0])
        if i == 1:
            ax[i].quiver(x1f0,x2f0,x3f0,0,0,qd,length=ql)
        elif i == 2:
            ax[i].quiver(x1f0,x2f0,x3f0,0,qd,0,length=ql)
        elif i == 3:
            ax[i].quiver(x1f0,x2f0,x3f0,qd,0,0,length=ql)
#        ax[i].scatter(x1f0,x2f0,x3f0,c=datas[i].flatten()[i0],s=10,edgecolors='none',norm=norms[i],cmap=cmaps[i],alpha=1,lw=0)
        fig.colorbar(axs[i])
    plt.show()

def testview():
    x = n.arange(10)
    x1,x2,x3 = n.meshgrid(x,x,x)
    data = x1 + x2*x3
    view(data)

def small_timestep_file(filename,size):
    #find region causing small timestep
    #look at velocities and density 
    data = cr.parsedata(cr.aread(filename))
    small_timestep_data(data,size)


def small_timestep_data(data,size):
    rho = data[3]
    v1 = data[5]
    v2 = data[6]
    v3 = data[7]
    vv = v1*v1 + v2*v2 + v3*v3
    shape = rho.shape
    coords = n.unravel_index(n.argmax(vv),shape)
    rho_s = slice_neigh(rho,coords,size)
    v1_s = slice_neigh(v1,coords,size)
    v2_s = slice_neigh(v2,coords,size)
    v3_s = slice_neigh(v3,coords,size)
    '''
    things = [rho,v1,v2,v3]
    names = ['rho','v1','v2','v3']
    name_i = 0
    for thing in things:
        print('viewing variable:',names[name_i])
        name_i += 1
        view(slice_neigh(thing,coords,size))
    '''
    view4([rho_s,v1_s,v2_s,v3_s])
stf = small_timestep_file
std = small_timestep_data

def slice_neigh(data,indices,size):
    x1,x2,x3 = indices
    return data[(x1-size):(x1+size+1),
                (x2-size):(x2+size+1),
                (x3-size):(x3+size+1)]

