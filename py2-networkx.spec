### RPM external py2-networkx 1.8.1
## INITENV +PATH PYTHONPATH %i/$PYTHON_LIB_SITE_PACKAGES
Source: https://pypi.python.org/packages/source/n/networkx/networkx-%realversion.tar.gz
Requires: python 
BuildRequires: py2-numpy py2-scipy py2-matplotlib

%prep
%setup -n networkx-%realversion

%build
python setup.py build

%install
python setup.py install --prefix=%i 
