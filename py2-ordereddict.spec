### RPM external py2-ordereddict 1.1
## INITENV +PATH PYTHONPATH %i/$PYTHON_LIB_SITE_PACKAGES
Source: https://pypi.python.org/packages/source/o/ordereddict/ordereddict-%realversion.tar.gz
Requires: python py2-setuptools

%prep
%setup -n ordereddict-%realversion

%build
python setup.py build

%install
python setup.py install --prefix=%i 
