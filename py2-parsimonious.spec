### RPM external py2-parsimonious 0.6.1
## INITENV +PATH PYTHONPATH %i/$PYTHON_LIB_SITE_PACKAGES
Source: https://pypi.python.org/packages/source/p/parsimonious/parsimonious-%realversion.tar.gz
Requires: python py2-setuptools

%prep
%setup -n parsimonious-%realversion

%build
python setup.py build

%install
python setup.py install --prefix=%i --single-version-externally-managed --record=/dev/null
