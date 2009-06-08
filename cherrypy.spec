### RPM external cherrypy 3.1.2
%define pythonv `echo $PYTHON_VERSION |cut -d. -f1,2`
## INITENV +PATH PYTHONPATH %i/lib/python%{pythonv}/site-packages

# use line below for version 2.2.1
#Source: http://switch.dl.sourceforge.net/sourceforge/%n/CherryPy-%v.tar.gz

# this is where cherrypy version 3 is located
Source: http://download.cherrypy.org/cherrypy/%v/CherryPy-%realversion.tar.gz
Requires: python

%prep
%setup -n CherryPy-%realversion
%build
%install
python setup.py install --prefix=%i
perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/cherryd
