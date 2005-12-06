# $Id$
#

############# SET THESE TO SUIT YOUR INSTALLATION ####################

# root of the installation tree: this is a reasonable default
ROOTDIR= /usr/local
# where to install pyformex: some prefer to use $(ROOTDIR)/lib
LIBDIR= $(ROOTDIR)
# where to create symbolic links to the executable files
BINDIR= $(ROOTDIR)/bin
# where to install the documentation
DOCDIR= $(ROOTDIR)/share/doc

############# NOTHING CONFIGURABLE BELOW THIS LINE ###################

VERSION= 0.2.1
PYFORMEXDIR= pyformex-$(VERSION)
INSTDIR= $(LIBDIR)/$(PYFORMEXDIR)
DOCINSTDIR= $(DOCDIR)/$(PYFORMEXDIR)
PROGRAM= pyformex
PYSOURCE= camera.py canvas.py colors.py draw.py flatdb.py flatkeydb.py \
  formex.py globaldata.py gui.py helpviewer.py lima.py pyfotemp.py turtle.py \
  units.py utils.py vector.py widgets.py
SOURCE= $(PYSOURCE) pyformexrc
ICONS= icons/*.xbm
HTMLDIR= doc/html
HTMLDOCS= $(addprefix $(HTMLDIR)/,$(PYSOURCE:.py=.html))
DOCFILES= README COPYING FAQ History
EXAMPLES= BarrelVault Baumkuchen Dome DoubleLayer Geodesic Hyparcap KochLine Lima Novation ParabolicTower ScallopDome Spiral Stars Torus
EXAMPLES2= TrussFrame tori
EXAMPLEFILES= $(addprefix examples/,$(addsuffix .py, $(EXAMPLES) $(EXAMPLES2) ))
IMAGEFILES =  $(addprefix screenshots/,$(addsuffix .png,$(EXAMPLES)))
STAMPABLE= README History Makefile TODO
NONSTAMPABLE= COPYING 
STAMP= Stamp 

.PHONY: install dist distclean

all:
	@echo "Do 'make install' to install pyformex"


############ User installation ######################

install:
	echo "config['docdir'] = '$(DOCINSTDIR)'" >> pyformexrc
	install -d $(INSTDIR) $(BINDIR) $(INSTDIR)/icons $(INSTDIR)/examples $(DOCINSTDIR) $(DOCINSTDIR)/html
	install -m 0664 $(SOURCE) $(INSTDIR)
	install -m 0775 $(PROGRAM) $(INSTDIR)
	install -m 0664 icons/* $(INSTDIR)/icons
	install -m 0664 examples/* $(INSTDIR)/examples
	install -m 0664 ${DOCFILES} $(DOCINSTDIR)
	install -m 0664 html/* $(DOCINSTDIR)/html
	ln -sfn $(INSTDIR)/$(PROGRAM) $(BINDIR)/$(PROGRAM)

uninstall:
	echo "There is no automatic uninstall procedure."""
	echo "Remove the entire pyformex directory from where you installed it."
	echo "Remove the symbolic link to the pyformex program."""
	echo "Remove the pyformex doc files."""

############ Creating Distribution ##################

vpath %.html $(HTMLDIR)

disttest:
	@cp -f Stamp.template Stamp.template.old && sed 's/pyformex .* Release/pyformex $(VERSION) Release/' Stamp.template.old > Stamp.template

dist:	dist.stamped

%.html: %.py
	pydoc -w ./$< && mv $@ $(HTMLDIR)


htmldoc: $(HTMLDOCS)

distdoc: htmldoc

stamp: Stamp.template
	$(STAMP) -tStamp.template version=$(VERSION) -oStamp.stamp

dist.stamped: distdoc distclean stamp
	mkdir $(PYFORMEXDIR) $(PYFORMEXDIR)/icons $(PYFORMEXDIR)/examples $(PYFORMEXDIR)/images $(PYFORMEXDIR)/html
	$(STAMP) -tStamp.stamp -d$(PYFORMEXDIR) $(PROGRAM) $(SOURCE)
	$(STAMP) -tStamp.stamp -d$(PYFORMEXDIR)/examples $(EXAMPLEFILES)
	$(STAMP) -tStamp.stamp -d$(PYFORMEXDIR) $(STAMPABLE)
	cp $(NONSTAMPABLE) $(PYFORMEXDIR)
	cp -R $(ICONS)  $(PYFORMEXDIR)/icons
	cp $(IMAGEFILES)  $(PYFORMEXDIR)/images
	cp $(HTMLDOCS) $(PYFORMEXDIR)/html
	tar czf $(PYFORMEXDIR).tar.gz $(PYFORMEXDIR)

distclean:
	rm -rf $(PYFORMEXDIR)
	alldirs . "rm -f *~"

#public: $(PYFORMEXDIR).tar.gz
#	scp README $(PYFORMEXDIR).tar.gz mecatrix.ugent.be:/home/ftp/pub/pyformex
