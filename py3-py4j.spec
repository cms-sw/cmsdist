### RPM external py3-py4j 0.9.1
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}

Source: https://pypi.python.org/packages/source/p/py4j/py4j-%{realversion}.tar.gz
Requires: python3
BuildRequires: py3-setuptools

%prep
%setup -n py4j-%realversion

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%i --single-version-externally-managed --record=/dev/null
find %i -name '*.egg-info' -exec rm {} \;
