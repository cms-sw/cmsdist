### RPM external py2-python-dateutil 1.1 
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}

Source: http://labix.org/download/python-dateutil/python-dateutil-%{realversion}.tar.bz2 
Requires: python

%prep
%setup -n python-dateutil-%{realversion} 

%build
python setup.py build

%install
python setup.py install --prefix=%i
find %i -name '*.egg-info' -exec rm {} \;
