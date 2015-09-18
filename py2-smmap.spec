### RPM external py2-smmap 0.9.0
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}

Source: https://pypi.python.org/packages/source/s/smmap/smmap-%realversion.tar.gz
Requires: python
BuildRequires: py2-setuptools

%prep
%setup -n smmap-%realversion

%build
python setup.py build

%install
python setup.py install --prefix=%i --single-version-externally-managed --record=/dev/null
find %i -name '*.egg-info' -print0 | xargs -0 rm -rf --
