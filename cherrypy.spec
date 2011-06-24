### RPM external cherrypy 3.1.2
## INITENV +PATH PYTHONPATH %i/$PYTHON_LIB_SITE_PACKAGES
Source: http://download.cherrypy.org/cherrypy/%v/CherryPy-%realversion.tar.gz
Requires: python

%prep
%setup -n CherryPy-%realversion

%build
python setup.py build

%install
python setup.py install --prefix=%i
find %i -name '*.egg-info' -exec rm {} \;
for f in %i/bin/cherryd; do perl -p -i -e 's{.*}{#!/usr/bin/env python} if $. == 1 && m{#!.*/bin/python}' $f; done
