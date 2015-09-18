### RPM external py2-gitdb 0.6.4
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}

Source: https://pypi.python.org/packages/source/g/gitdb/gitdb-%realversion.tar.gz
Requires: python py2-smmap
BuildRequires: py2-setuptools

%prep
%setup -n gitdb-%realversion

%build
python setup.py build

%install
python setup.py install --prefix=%i --record=/dev/null
find %i -name '*.egg-info' -print0 | xargs -0 rm -rf --
