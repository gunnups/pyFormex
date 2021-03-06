# $Id$
##
##  This file is part of pyFormex 0.8.9  (Fri Nov  9 10:49:51 CET 2012)
##  pyFormex is a tool for generating, manipulating and transforming 3D
##  geometrical models by sequences of mathematical operations.
##  Home page: http://pyformex.org
##  Project page:  http://savannah.nongnu.org/projects/pyformex/
##  Copyright 2004-2012 (C) Benedict Verhegghe (benedict.verhegghe@ugent.be) 
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
"""Tools for handling collections of elements belonging to multiple parts.

This module defines the Collection class.
"""
from __future__ import print_function

import pyformex as pf
from arraytools import *

################# Collection of Actors or Actor Elements ###############

class Collection(object):
    """A collection  is a set of (int,int) tuples.

    The first part of the tuple has a limited number of values and are used
    as the keys in a dict.
    The second part can have a lot of different values and is implemented
    as an integer array with unique values.
    This is e.g. used to identify a set of individual parts of one or more
    OpenGL actors.
    """
    def __init__(self):
        self.d = {}
        self.obj_type = None

    def setType(self,obj_type):
        self.obj_type = obj_type

    def clear(self,keys=[]):
        if keys:
            for k in keys:
                k = int(k)
                if k in self.d.keys():
                    del self.d[k]
        else:
            self.d = {}

    def add(self,data,key=-1):
        """Add new data to the collection.

        data can be a 2d array with (key,val) tuples or a 1-d array
        of values. In the latter case, the key has to be specified
        separately, or a default value will be used.
        """
        if len(data) == 0:
            return
        data = asarray(data)
        if data.ndim == 2:
            for key in unique(data[:,0]):
                self.add(data[data[:,0]==key,1],key)

        else:
            key = int(key)
            data = unique(data)
            if key in self.d:
                self.d[key] = union1d(self.d[key],data)
            elif data.size > 0:
                self.d[key] = data

    def set(self,data,key=-1):
        """Set the collection to the specified data.

        This is equivalent to clearing the corresponding keys
        before adding.
        """
        self.clear()
        self.add(data,key)

    def remove(self,data,key=-1):
        """Remove data from the collection."""
        data = asarray(data)
        if data.ndim == 2:
            for key in unique(data[:,0]):
                self.remove(data[data[:,0]==key,1],key)

        else:
            key = int(key)
            if key in self.d:
                data = setdiff1d(self.d[key],unique(data))
                if data.size > 0:
                    self.d[key] = data
                else:
                    del self.d[key]
            else:
                pf.debug("Not removing from non-existing selection for actor %s" % key,pf.DEBUG.DRAW)
    
    def has_key(self,key):
        """Check whether the collection has an entry for the key."""
        return key in self.d

    def __setitem__(self,key,data):
        """Set new values for the given key."""
        key = int(key)
        data = unique(data)
        if data.size > 0:
            self.d[key] = data
        else:
            del self.d[key]

    def __getitem__(self,key):
        """Return item with given key."""
        return self.d[key]

    def get(self,key,default=[]):
        """Return item with given key or default."""
        key = int(key)
        return self.d.get(key,default)


    def keys(self):
        """Return a sorted array with the keys"""
        k = asarray(self.d.keys())
        k.sort()
        return k

    def items(self):
        """Return a zipped list of keys and values."""
        return self.d.items()
        
    def __str__(self):
        s = ''
        keys = self.d.keys()
        keys.sort()
        for k in keys:
            s += "%s %s; " % (k,self.d[k])
        return s


################# Testing ###############

if __name__ == "__main__":
    print("Testing the Collection object")
    a = Collection()
    a.add(range(7),3)
    a.add(range(4))
    a.remove([2,4],3)
    print(a)
    a.add([[2,0],[2,3],[-1,7],[3,88]])
    print(a)
    a[2] = [1,2,3]
    print(a)
    a[2] = []
    print(a)
    a.set([[2,0],[2,3],[-1,7],[3,88]])
    print(a)

                    
# End
