### RPM external py2-docutils 0.9.1
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}

Source0: svn://docutils.svn.sourceforge.net/svnroot/docutils/trunk/sandbox/rst2wiki@7467?scheme=https&strategy=export&module=sandbox&output=/rst2wiki.tar.gz
Source1: http://downloads.sourceforge.net/docutils/docutils-%{realversion}.tar.gz
Requires: python

%prep
%setup -T -b 0 -n sandbox
%setup -D -T -b 1 -n docutils-%realversion

%build
python setup.py build

%install
python setup.py install --prefix=%i
cp ../sandbox/tools/rst2wiki.py %i/bin/
cp ../sandbox/docutils/writers/wiki.py %i/$PYTHON_LIB_SITE_PACKAGES/docutils/writers/
python -m compileall %i/$PYTHON_LIB_SITE_PACKAGES
for f in %i/bin/rst*; do perl -p -i -e 's{.*}{#!/usr/bin/env python} if $. == 1 && m{#!.*/bin/python}' $f; done
