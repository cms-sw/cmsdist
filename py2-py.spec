### RPM external py2-py 1.4.31
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}
Source: http://pypi.python.org/packages/source/p/py/py-%{realversion}.tar.gz
Requires: python
BuildRequires: py2-setuptools

%prep
%setup -n py-%{realversion}

%build
python setup.py build

%install
python setup.py install --prefix=%i --single-version-externally-managed --record=/dev/null
find %i -name '*.egg-info' -exec rm {} \;
