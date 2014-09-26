### RPM external py2-futures 2.2.0
## INITENV +PATH PYTHONPATH %i/$PYTHON_LIB_SITE_PACKAGES
Source: https://pypi.python.org/packages/source/f/futures/futures-%realversion.tar.gz
Requires: python py2-setuptools

%prep
%setup -n futures-%realversion

%build
python setup.py build

%install
python setup.py install --prefix=%i  --single-version-externally-managed --record=/dev/null
