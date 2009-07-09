#!/usr/bin/env python
# $Id$
"""
sloc.py

Create a sloccount report for the pyformex tagged releases.
(C) Benedict Verhegghe
"""

print __doc__
from pyformex.flatkeydb import FlatDB
import os,sys,commands,datetime

now = datetime.datetime.now()
print now

curdir = os.path.dirname(__file__)
dbfile = os.path.join(curdir,'pyformex-releases.fdb')
if not os.path.exists(dbfile):
    print("The dbfile %s does not exist"%dbfile)
    sys.exit()
    
DB = FlatDB(req_keys=['tag','date','rev'],beginrec = 'release',endrec = '')

DB.readFile(dbfile)
keys = DB.keys()
keys.sort()

print "List of releases: %s" % keys

tmpdir = '_sloccount_'
workdir = os.path.join(curdir,tmpdir)


def runCmd(cmd):
    print cmd
    return commands.getstatusoutput(cmd)


def sloccount(rel):
    """Create a sloccount report for release"""
    tag = rel['tag']
    rev = rel['rev']
    print "Processing release %s" % tag

    slocfile = "pyformex.sloc.%s" % tag
    if os.path.exists(slocfile):
        print "  %s exists: skipping" % slocfile
        return
        
    if not os.path.exists(workdir):
        cmd = "svn co svn://svn.berlios.de/pyformex/trunk -r%s %s" % (rev,tmpdir)
        runCmd(cmd)

    cmd = "cd %s;svn up -r%s" % (tmpdir,rev)
    runCmd(cmd)

    pyfdir = os.path.join(tmpdir,'pyformex')
    if not os.path.isdir(pyfdir):
        pyfdir = tmpdir
    print "SLOCCOUNTING %s" % pyfdir
    cmd = "sloccount %s > %s" % (pyfdir,slocfile)
    runCmd(cmd)
    


for release in keys:
    sloccount(DB[release])
    

# Now, create some statistics

def extract(filename):
    res,out = runCmd("gawk -f slocstats.awk %s" % filename)
    if res:
        raise ValueError,"Error extracting data"
    return dict([ DB.splitKeyValue(line) for line in out.split('\n') ])

KEYS=set([])
for release in keys:
    rel = DB[release]
    tag = rel['tag']
    rev = rel['rev']
    slocfile = "pyformex.sloc.%s" % tag
    print "Processing %s" % slocfile
    rel.update(extract(slocfile))
    KEYS |= set(rel.keys())

# No, better use a standard order!
KEYSorted = "date rev tag size python ansic sh sloc manyears years dollars"
KEYS = KEYSorted.split()

DB.writeFile('pyformex-stats.db')

out = "#"+' '.join(KEYS)+'\n'

for release in keys:
    rel = DB[release]
    val = [ rel.get(k,'*') for k in KEYS ]
    out += ' '.join(val)+'\n'

print out
statsfile = file('pyformex-stats.dat','w')
statsfile.write(out)
statsfile.close()

gnu = """set terminal png size 640,480
set output "pyformex-stats.png"
set datafile missing '*'
set title "pyFormex history (http://pyformex.berlios.de)\nCreated %s"
set key top left
#set offsets 0,0.1,0,0
set xdata time
set timefmt "%Y-%m-%d"
set format x "%y-%m"
set xlabel "Date (YY-MM)"
set ylabel "revision number"
#set yrange [0:1.2]
plot """ % now

KEYSplot = "size python ansic sh sloc manyears dollars"

for i,key in enumerate(KEYSplot.split()):
    col = KEYSorted.index(key) + 1
    gnu += "\\\n  'pyformex-stats.dat' using %s:1 title '%s' with lines linetype %s" % (col,key,i)

print gnu
#gnufile =  file('pyformex-stats.gnu','w')

# End