# Some tools that add functionality to athena_read
# that may be useful while reading data 

import numpy as n
import os
import athena_read as ar
def aread(filename):
    suffix = filename.split('.')[-1]
    if suffix == 'vtk':
        return ar.vtk(filename)
    if suffix == 'tab':
        return ar.tab(filename)
    if suffix == 'athdf':
        return ar.athdf(filename,subsample=True)
    else:
        print('Error: filetype not supported')
        return

def cyltocart(r,phi,z):
    #phi is azimuthal angle
    x = r*n.cos(phi)
    y = r*n.sin(phi)
    return x,y,z

def sphtocart(r,theta,phi):
    #theta is polar angle
    #phi is azimuthal angle
    cylr = n.sin(theta)
    x = cylr*n.cos(phi)
    y = cylr*n.sin(phi)
    z = r*n.cos(theta)
    return x,y,z

def data_coord(data):
    if (type(data) == dict) or (type(data) == ar.athdf):
        if 'x1v' in data.keys():
            x1 = data['x1v']
            x2 = data['x2v']
            x3 = data['x3v']
        elif 'x1f' in data.keys():
            x1 = data['x1f']
            x2 = data['x2f']
            x3 = data['x3f']
        else:
            x1 = False
            x2 = False
            x3 = False
    if type(data) == tuple:
        x1 = data[0]
        x2 = data[1]
        x3 = data[2]
    return x1.copy(),x2.copy(),x3.copy()


def data_rho(data):
    if (type(data) == dict) or (type(data) == ar.athdf):
        if 'rho' in data.keys():
            rho = data['rho']
        elif 'dens' in data.keys():
            rho = data['dens']
        else:
            rho = False
    if type(data) == tuple:
        if 'rho' in data[3].keys():
            rho = data[3]['rho']
        elif 'dens' in data[3].keys():
            rho = data[3]['dens']
        else:
            rho = False
    return rho

def data_phi(data):
    if type(data) == dict:
        phi = data['Phi']
    if type(data) == tuple:
        if 'Phi' in data[3].keys():
            phi = data[3]['Phi']
        else:
            phi = False
    return phi

def parsedata(data):
    if type(data) == dict:
        if 'x1v' in data.keys():
            x1 = data['x1v']
            x2 = data['x2v']
            x3 = data['x3v']
        elif 'x1f' in data.keys():
            x1 = data['x1f']
            x2 = data['x2f']
            x3 = data['x3f']
        else:
            x1 = False
            x2 = False
            x3 = False
        if 'rho' in data.keys():
            rho = data['rho']
        elif 'dens' in data.keys():
            rho = data['dens']
        else:
            rho = False
        if 'press' in data.keys():
            press = data['press']
        elif 'Etot' in data.keys():
            press = data['Etot']
        else:
            press = False
        if 'vel1' in data.keys():
            v1 = data['vel1']
            v2 = data['vel2']
            v3 = data['vel3']
        elif 'mom1' in data.keys():
            v1 = data['mom1']/rho
            v2 = data['mom2']/rho
            v3 = data['mom3']/rho
        if 'Bcc1' in data.keys():
            bcc1 = data['Bcc1']
            bcc2 = data['Bcc2']
            bcc3 = data['Bcc3']
            bccbool = True
        else:
            bcc1 = 0.0*v1
            bcc2 = 0.0*v1
            bcc3 = 0.0*v1
            bccbool = False
    if type(data) == tuple:
        x1 = data[0]
        x2 = data[1]
        x3 = data[2]
        if 'rho' in data[3].keys():
            rho = data[3]['rho']
        elif 'dens' in data[3].keys():
            rho = data[3]['dens']
        else:
            rho = False
        if 'press' in data[3].keys():
            press = data[3]['press']
        else:
            press = 1.0*rho
        if 'vel' in data[3].keys():
            vel = data[3]['vel']
            v1 = vel[:,:,:,0]
            v2 = vel[:,:,:,1]
            v3 = vel[:,:,:,2]
        elif 'mom' in data[3].keys():
            vel = data[3]['mom']
            v1 = vel[:,:,:,0]/rho
            v2 = vel[:,:,:,1]/rho
            v3 = vel[:,:,:,2]/rho
        else:
            v1 = False
            v2 = False
            v3 = False

        if 'Bcc' in data[3].keys():
            bccbool = True
            bcc = data[3]['Bcc']
            bcc1 = bcc[:,:,:,0]
            bcc2 = bcc[:,:,:,1]
            bcc3 = bcc[:,:,:,2]
        else:
            bccbool = False
            bcc1 = False
            bcc2 = False
            bcc3 = False
    return x1,x2,x3,rho,press,v1,v2,v3,bcc1,bcc2,bcc3

def data_to_dict(data):
    output = {}
    datalist = parsedata(data)
    keys = ['x1','x2','x3','rho','press','v1','v2','v3','bcc1','bcc2','bcc3']
    for i in range(len(keys)):
        output[keys[i]] = datalist[i]
    return output

## Grab all the filenames in the directory, sort them, and put them in a list
def getfiles(suffix):
    prefilenames = n.sort(os.listdir('.'))
    filenames = []
    for prefile in prefilenames:
        if prefile.split('.')[-1] == suffix:
#        if prefile.find(suffix) > -1:
            filenames += [prefile]
    print(filenames)
    return filenames


