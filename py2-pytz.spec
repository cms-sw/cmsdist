### RPM external py2-pytz 2016.3 
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}

Source: http://cheeseshop.python.org/packages/source/p/pytz/pytz-%{realversion}.tar.bz2 
Requires: python

%prep
%setup -n pytz-%{realversion}

%build
python setup.py build

%install
python setup.py install --prefix=%i
