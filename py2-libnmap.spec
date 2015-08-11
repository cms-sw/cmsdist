### RPM external py2-libnmap 0.6.2
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}

Source: https://pypi.python.org/packages/source/p/python-libnmap/python-libnmap-%realversion.tar.gz 
Requires: python nmap
BuildRequires: py2-setuptools

%prep
%setup -n python-libnmap-%realversion

%build
python setup.py build

%install
python setup.py install --prefix=%i --record=/dev/null
find %i -name '*.egg-info' -print0 | xargs -0 rm -rf --
