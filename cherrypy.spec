### RPM external cherrypy 3.0.1
%define pythonv %(echo $PYTHON_VERSION |cut -d. -f1,2)
## INITENV +PATH PYTHONPATH %i/lib/python$(echo $PYTHON_VERSION |cut -d. -f 1,2)/site-packages

# use line below for version 2.2.1
#Source: http://switch.dl.sourceforge.net/sourceforge/%n/CherryPy-%v.tar.gz

# this is where cherrypy version 3 is located
Source: http://download.cherrypy.org/cherrypy/%v/CherryPy-%v.tar.gz
Requires: python

%prep
%setup -n CherryPy-%v
%build
%install
python setup.py install --prefix=%i
