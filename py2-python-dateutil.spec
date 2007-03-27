### RPM external py2-python-dateutil 1.1 
%define pythonv %(echo $PYTHON_VERSION | cut -f1,2 -d.)
## INITENV +PATH PYTHONPATH %i/lib/python`echo $PYTHON_VERSION | cut -f1,2 -d.`/site-packages

Source: http://labix.org/download/python-dateutil/python-dateutil-%{v}.tar.bz2 
Requires: python

%prep
%setup -n python-dateutil-%{v} 
%build
%install
python setup.py install --prefix=%i
