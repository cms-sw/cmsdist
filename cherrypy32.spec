### RPM external cherrypy32 3.2.2
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}
Source: http://download.cherrypy.org/cherrypy/%v/CherryPy-%realversion.tar.gz
Requires: python
Patch0: cherrypy-multipart-length-32

%prep
%setup -n CherryPy-%realversion
%patch0 -p0
perl -p -i -e 's/import profile/import cProfile as profile/' cherrypy/lib/profiler.py

%build
python setup.py build

%install
python setup.py install --prefix=%i
find %i -name '*.egg-info' -exec rm {} \;
for f in %i/bin/cherryd; do perl -p -i -e 's{.*}{#!/usr/bin/env python} if $. == 1 && m{#!.*/bin/python}' $f; done
