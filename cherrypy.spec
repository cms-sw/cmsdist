### RPM external cherrypy 5.4.0
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}
Source: http://github.com/cherrypy/cherrypy/archive/v%realversion.tar.gz
Requires: python
Patch0: cherrypy-multipart-length

%prep
%setup -n cherrypy-%realversion
%patch0 -p0
perl -p -i -e 's/import profile/import cProfile as profile/' cherrypy/lib/profiler.py

%build
python setup.py build

%install
mkdir -p %i/$PYTHON_LIB_SITE_PACKAGES
PYTHONPATH=%i/$PYTHON_LIB_SITE_PACKAGES:$PYTHONPATH \
python setup.py install --prefix=%i
perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/cherryd
perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/lib/python2.7/site-packages/CherryPy-5.4.0.post20201110-py2.7.egg/EGG-INFO/scripts/cherryd
perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/lib/python2.7/site-packages/CherryPy-5.4.0.post20201110-py2.7.egg/cherrypy/cherryd
