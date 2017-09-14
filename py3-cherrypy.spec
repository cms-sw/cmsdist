### RPM external py3-cherrypy 5.4.0
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}
Source: http://github.com/cherrypy/cherrypy/archive/v%realversion.tar.gz
Requires: python3
Patch0: cherrypy-multipart-length

%prep
%setup -n cherrypy-%realversion
%patch0 -p0
perl -p -i -e 's/import profile/import cProfile as profile/' cherrypy/lib/profiler.py

%build
python3 setup.py build

%install
mkdir -p %i/$PYTHON_LIB_SITE_PACKAGES
PYTHONPATH=%i/$PYTHON_LIB_SITE_PACKAGES:$PYTHONPATH \
python3 setup.py install --prefix=%i
find %i -name '*.egg-info' -exec rm {} \;
files=`find %i -name cherryd`
for f in $files; do perl -p -i -e 's{.*}{#!/usr/bin/env python3} if $. == 1 && m{#!.*/bin/python}' $f; done
#for f in %i/bin/cherryd; do perl -p -i -e 's{.*}{#!/usr/bin/env python3} if $. == 1 && m{#!.*/bin/python}' $f; done
