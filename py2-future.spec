### RPM external py2-future 0.14.3
## INITENV +PATH PYTHONPATH %i/$PYTHON_LIB_SITE_PACKAGES
Source: https://pypi.python.org/packages/source/f/future/future-%realversion.tar.gz
Requires: python py2-setuptools

%prep
%setup -n future-%realversion

%build
python setup.py build

%install
python setup.py install 
