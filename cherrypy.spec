### RPM external cherrypy 2.2.1
%define pythonv %(echo $PYTHON_VERSION |cut -d. -f1,2)
## INITENV +PATH PYTHONPATH %i/lib/python%{pythonv}/site-packages
Source: http://switch.dl.sourceforge.net/sourceforge/%n/CherryPy-%v.tar.gz
Requires: python

%prep
%setup -n CherryPy-%v
%build
%install
python setup.py install --prefix=%i
