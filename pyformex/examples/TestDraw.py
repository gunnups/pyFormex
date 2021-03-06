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
"""TestDraw

Example for testing the low level drawing functions
"""
from __future__ import print_function
_status = 'checked'
_level = 'normal'
_topics = ['geometry','mesh','drawing']
_techniques = ['widgets','dialog','random','color']

from gui.draw import *

from numpy.random import rand
    
setDrawOptions({'clear':True, 'bbox':'auto'})
linewidth(2) # The linewidth option is not working nyet

geom_mode = [ 'Formex','Mesh' ]
plexitude = [ 1,2,3,4,5,6,8 ]
element_type = [ 'auto', 'tet4', 'wedge6', 'hex8' ]
color_mode = [ 'none', 'single', 'element', 'vertex' ]

# The points used for a single element of plexitude 1..8
Points = {
    1: [[0.,0.,0.]],
    2: [[0.,0.,0.],[1.,0.,0.]],
    3: [[0.,0.,0.],[1.,0.,0.],[0.,1.,0.]],
    4: [[0.,0.,0.],[1.,0.,0.],[1.,1.,0.],[0.,1.,0.]],
    5: [[0.,0.,0.],[1.,0.,0.],[1.5,0.5,0.],[1.,1.,0.],[0.,1.,0.]],
    6: [[0.,0.,0.],[1.,0.,0.],[1.5,0.5,0.],[1.,1.,0.],[0.,1.,0.],[-0.2,0.5,0.]],
    'tet4': [[0.,0.,0.],[1.,0.,0.],[0.,1.,0.],[0.,0.,1.]],
    'wedge6': [[0.,0.,0.],[1.,0.,0.],[0.,1.,0.],[0.,0.,1.],[1.,0.,1.],[0.,1.,1.]],
    'hex8': [[0.,0.,0.],[1.,0.,0.],[1.,1.,0.],[0.,1.,0.],[0.,0.,1.],[1.,0.,1.],[1.,1.,1.],[0.,1.,1.]],
    }


def select_geom(geom,nplex,eltype):
    """Construct the geometry"""
    try:
        nplex = int(eltype[-1])
    except:
        if not nplex in Points.keys():
            nplex = max([i for i in plexitude if i in Points.keys()])
        eltype = None
    if eltype is None:
        x = Points[nplex]
    else:
        x = Points[eltype]
    F = Formex([x],eltype=eltype).replic2(2,2,2.,2.)
    if geom == 'Formex':
        return F
    else:
        return F.toMesh()
    

def select_color(F,color):
    """Create a set of colors for object F"""
    if color == 'single':
        shape = (1,3)
    elif color == 'element':
        shape = (F.nelems(),3)
    elif color == 'vertex':
        shape = (F.nelems(),F.nplex(),3)
    else:
        return None
    return rand(*shape)

geom = 'Formex'
nplex = 3
eltype = 'auto'
color = 'element'
pos = None
items = [
    _I('geom',geom,'radio',choices=geom_mode,text='Geometry Model'),
    _I('nplex',nplex,'select',choices=plexitude,text='Plexitude'),
    _I('eltype',eltype,'select',choices=element_type,text='Element Type'),
    _I('color',color,'select',choices=color_mode,text='Color Mode'),
    ]

dialog = None


def show():
    """Accept the data and draw according to them"""
    dialog.acceptData()
    res = dialog.results
    res['nplex'] = int(res['nplex'])
    globals().update(res)

    G = select_geom(geom,nplex,eltype)
    print("GEOM: nelems=%s, nplex=%s" % (G.nelems(),G.nplex()))
    C = select_color(G,color)
    if C is not None:
        print("COLORS: shape=%s" % str(C.shape))
    draw(G,color=C,clear=True)


def close():
    global dialog
    if dialog:
        dialog.close()
        dialog = None
    scriptRelease(__file__)


def timeOut():
    """What to do on a InputDialog timeout event.

    As a policy, all pyFormex examples should behave well on a
    dialog timeout.
    Most users can simply ignore this.
    """
    show()
    close()

def run():
    global dialog
    clear()
    lights(False)
    # Create the non-modal dialog widget and show it
    dialog = Dialog(items,caption='Drawing parameters',actions = [('Close',close),('Show',show)],default='Show')
    dialog.timeout = timeOut
    dialog.show()
    scriptLock(__file__)
        
if __name__ == 'draw':
    run()
# End
