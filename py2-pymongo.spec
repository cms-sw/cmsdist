### RPM external py2-pymongo 2.7.1
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}

Source: http://pypi.python.org/packages/source/p/pymongo/pymongo-%realversion.tar.gz
Requires: python elementtree
BuildRequires: py2-setuptools

%prep
%setup -n pymongo-%realversion

%build
python setup.py build

%install
python setup.py install --prefix=%i --single-version-externally-managed --record=/dev/null
find %i -name '*.egg-info' -exec rm {} \;
