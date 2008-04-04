#!/usr/bin/env pyformex --hui
# $Id$

from numpy import *


def build_matrix(atoms,x,y=0,z=0):
    """Build a matrix of functions of coords.

    Atoms is a list of text strings representing some function of
    x(,y)(,z). x is a list of x-coordinats of the nodes, y and z can be set
    to lists of y,z coordinates of the nodes.
    Each line of the returned matrix contains the atoms evaluated at a
    node.
    """
    aa = zeros((len(x),len(atoms)),Float)
    for k,a in enumerate(atoms):
        aa[:,k] = eval(a)
    return aa   


def isopar(F,type,coords,oldcoords):
    """Apply isoparametric transform.
    
    """
    isodata = {
        'tri3'  : (2, ('1','x','y')),
        'quad4' : (2, ('1','x','y','x*y')),
        'tri6'  : (2, ('1','x','y','x*y','x*x','y*y')),
        'quad8' : (2, ('1','x','y','x*y','x*x','y*y','x*x*y','x*y*y')),
        'quad9' : (3, ('1','x','y','x*y','x*x','y*y','x*x*y','x*y*y','x*x*y*y'))
        }
    ndim,atoms = isodata[type]
    if isinstance(coords,Formex):
        coords = reshape(coords.nodes().data(),(-1,3))
    if isinstance(oldcoords,Formex):
        oldcoords = reshape(oldcoords.nodes().data(),(-1,3))
    #print oldcoords
    x = oldcoords[:,0]
    if ndim > 1:
        y = oldcoords[:,1]
    else:
        y = 0
    if ndim > 2:
        z = oldcoords[:,2]
    else:
        z = 0
    #print "new=",coords
    #print "old=",oldcoords
    aa = build_matrix(atoms,x,y,z)
    #print "aa=", aa
    ab = linalg.solve(aa,coords)
    #print "ab=",ab
    x = F.x().ravel()
    if ndim > 1:
        y = F.y().ravel()
    else:
        y = 0
    if ndim > 2:
        z = F.z().ravel()
    else:
        z = 0
    aa = build_matrix(atoms,x,y,z)
    #print "aa=", aa
    xx = dot(aa,ab)
    return Formex(reshape(xx,F.shape()))


def base(type,m,n=None):
    """A regular pattern for type.

    type = 'tri' or 'quad'(default) or 'triline' or 'quadline'
    m = number of cells in direction 0
    n = number of cells in direction 1
    """
    n = n or m
    if type == 'triline':
        return Formex(pattern('164')).replic2(m,n,1,1,0,1,0,-1)
    elif type == 'quadline':
        return Formex(pattern('2')).replic2(m+1,n,1,1) + \
               Formex(pattern('1')).replic2(m,n+1,1,1)
    elif type == 'tri':
        return Formex(mpattern('12-34')).replic2(m,n)
    else:
        return Formex(mpattern('123')).replic2(m,n)


F = base('quad',10,10)
clear()
message('This is the base pattern in natural coordinates')
draw(F)
ll,ur = F.bbox()
sc = array(ur)-array(ll)
sc[2] = 10.
x1 = Formex([[[0,0,0]]]).replic2(3,3,.5,.5)
x2 = x1.copy()
for i in [4]:
    x2[i] += [[0.2,0,0.2]]
x1 = x1.scale(sc)
x2 = x2.scale(sc)
clear()
message('This is the set of nodes in cartesian coordinates')
draw(x2)

G = isopar(F,'quad9',x2.nodes(),x1.nodes())
G.setProp(1)

clear()
draw(F)
draw(G)


clear()
#draw(F)
draw(G)

# End