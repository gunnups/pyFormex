#!/usr/bin/env pyformex
# $Id$
##
##  This file is part of pyFormex 0.8.1 Release Wed Dec  9 11:27:53 2009
##  pyFormex is a tool for generating, manipulating and transforming 3D
##  geometrical models by sequences of mathematical operations.
##  Homepage: http://pyformex.org   (http://pyformex.berlios.de)
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
"""TextGravity

Show the use of the text gravity parameter.

level = 'beginner'
topics = []
techniques = ['text']

"""

clear()
lights(False)
x = GD.canvas.width()//2
y = GD.canvas.height()//2
x,y = 600,300
print x,y

from gui.decors import Grid

d = 50

G = Grid(x-50,y-50,x+50,y+50,2,2)
decorate(G)
    
for g in [ 'NW','N','NE','W','C','E','SW','S','SE']:
    T = drawText("XXX  %s  XXX"%g,x,y,gravity=g)
    sleep(2)
    undecorate(T)


from gui.gluttext import GLUTFONTS
for f in GLUTFONTS.keys():
    S = drawText(f,20,20,font='hv18')
    T = drawText('X',x,y,font=f,gravity='C')
    sleep(1)
    undecorate(S)
    undecorate(T)
    
# End