# $Id$
##
##  This file is part of pyFormex 0.8.5     Sun Nov  6 17:27:05 CET 2011
##  pyFormex is a tool for generating, manipulating and transforming 3D
##  geometrical models by sequences of mathematical operations.
##  Home page: http://pyformex.org
##  Project page:  https://savannah.nongnu.org/projects/pyformex/
##  Copyright (C) Benedict Verhegghe (benedict.verhegghe@ugent.be) 
##  Distributed under the GNU General Public License version 3 or later.
##
##
##  This program is free software: you can redistribute it and/or modify
##  it under the terms of the GNU General Public License as published by
##  the Free Software Foundation, either version 3 of the License, or
##  (at your option) any later version.
##
##  This program is distributed in the hope that it will be useful,
##  but WITHOUT ANY WARRANTY; without even the implied warranty of
##  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##  GNU General Public License for more details.
##
##  You should have received a copy of the GNU General Public License
##  along with this program.  If not, see http://www.gnu.org/licenses/.
##
"""read/write tetgen format files."""

import os
import utils
from formex import *
from filewrite import *

def invalid(line,fn):
    """Print message for invalid line."""
    print("The following line in file %s is invalid:" % fn)
    print(line)
    

def readNodes(fn):
    """Read a tetgen .node file.

    Returns a tuple of two arrays: nodal coordinates and node numbers.
    """
    fil = open(fn,'r')
    line = fil.readline()
    s = line.strip('\n').split()
    npts,ndim,nattr,nbmark = map(int,s)
    nodes = fromfile(fil,sep=' ',dtype=Float,count=npts*(ndim+1)).reshape((npts,ndim+1))
    return nodes[:,1:],nodes[:,0].astype(int32)


def readElems(fn):
    """Read a tetgen .ele file.

    Returns a tuple of 3 arrays:
      elems : the element connectivity
      elemnr : the element numbers
      attr: the element attributes.
    """
    fil = open(fn,'r')
    line = fil.readline()
    s = line.strip('\n').split()
    nelems,nplex,nattr = map(int,s)
    elems = fromfile(fil,sep=' ',dtype=int32,count=(nplex+1)*nelems).reshape((nelems,nplex+nattr+1))
    return elems[:,1:nplex+1],elems[:,0],elems[:,nplex+1:]


def readFaces(fn):
    """Read a tetgen .face file.

    Returns an array of triangle elements.
    """
    fil = open(fn,'r')
    line = fil.readline()
    s = line.strip('\n').split()
    nelems,bmark = map(int,s[:2])
    ncols = 4 + bmark
    elems = fromfile(fil,sep=' ',dtype=int32, count=ncols*nelems)
    elems = elems.reshape((-1,ncols))
    return elems[:,1:4]


def readSmesh(fn):
    """Read a tetgen .smesh file.

    Returns an array of triangle elements.
    """
    fil = open(fn,'r')
    part = 0
    elems = None
    line = fil.readline()
    while not line.startswith('# part 2:'):
        line = fil.readline()
    line = fil.readline()
    s = line.strip('\n').split()
    nelems = int(s[0])
    elems = fromfile(fil,sep=' ',dtype=int32, count=4*nelems)
    elems = elems.reshape((-1,4))
    return elems[:,1:]


def readSurface(fn):
    """Read a tetgen surface from a .node/.face file pair.

    The given filename is either the .node or .face file.
    Returns a tuple of (nodes,elems).
    """
    nodes,numbers = readNodes(utils.changeExt(fn,'.node'))
    print("Read %s nodes" % nodes.shape[0])
    elems = readFaces(utils.changeExt(fn,'.face'))
    print("Read %s elems" % elems.shape[0])
    #if numbers[0] == 1:
    #    elems -= 1 
    return nodes,elems


def readNeigh(fn):
    """Read a tetgen .neigh file.

    Returns an arrays containing the tetrahedra neighbours:
    """
    fil = open(fn,'r')
    line = fil.readline()
    s = line.strip('\n').split()
    nelems, nneigh = map(int,s)
    elems = fromfile(fil,sep=' ',dtype=int32).reshape((nelems,nneigh+1))
    return elems[:,1:]


def writeNodes(fn,coords,offset=0):
    """Write a tetgen .node file."""
    coords = asarray(coords).reshape((-1,3))
    fil = open(fn,'w')
    fil.write("%d %d 0 0\n" % coords.shape)
    writeIData(coords,fil,"%f ",ind=offset)
    fil.close()


def writeSmesh(fn,facets,coords=None,holes=None,regions=None):
    """Write a tetgen .smesh file.

    Currently it only writes the facets of a triangular surface mesh.
    Coords should be written independently to a .node file.
    """
    fil = open(fn,'w')
    fil.write("# part 1: node list.\n")
    if coords is None:
        fil.write("0  3  0  0  # coords are found in %s.node.\n")
    fil.write("# part 2: facet list.\n")
    fil.write("%s 0\n" % facets.shape[0])
    for i,n in enumerate(facets):
        # adding comments breaks fast readback
        # fil.write("3 %s %s %s # %s\n" % (n[0],n[1],n[2],i))
        fil.write("3 %s %s %s\n" % (n[0],n[1],n[2]))
    fil.write("# part 3: hole list.\n")
    if holes is None:
        fil.write("0\n")
    fil.write("# part 4: region list.\n")
    if regions is None:
        fil.write("0\n")
    fil.write("# Generated by pyFormex\n")


def writeSurface(fn,coords,elems):
    """Write a tetgen surface model to .node and .smesh files.

    The provided file name is the .node or the .smesh filename.
    """
    writeNodes(utils.changeExt(fn,'.node'),coords)
    writeSmesh(utils.changeExt(fn,'.smesh'),elems)



def nextFilename(fn):
    """Returns the next file name in a family of tetgen file names."""
    m = re.compile("(?P<base>.*)\.(?P<id>\d*)\.(?P<ext>.*)").match(fn)
    if m:
        return "%s.%s.%s" % (m.group('base'),int(m.group('id'))+1,m.group('ext'))
    else:
        return '.1'.join(os.path.splitext(fn))


def runTetgen(fn):
    """Run tetgen mesher on the specified file.

    The input file is a closed triangulated surface.
    tetgen will generate a volume tetraeder mesh inside the surface,
    and create a new approximation of the surface as a by-product.
    """
    if os.path.exists(fn):
        sta,out = utils.runCommand('tetgen -z %s' % fn)
    
# End
