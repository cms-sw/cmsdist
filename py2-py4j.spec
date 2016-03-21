### RPM external py2-py4j 0.9.1
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}

Source: https://pypi.python.org/packages/source/p/py4j/py4j-%{realversion}.tar.gz
Requires: python
BuildRequires: py2-setuptools

%prep
%setup -n py4j-%realversion

%build
python setup.py build

%install
python setup.py install --prefix=%i --single-version-externally-managed --record=/dev/null
find %i -name '*.egg-info' -exec rm {} \;
