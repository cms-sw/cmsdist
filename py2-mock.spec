### RPM external py2-mock 1.3.0
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}

Source: https://pypi.python.org/packages/source/m/mock/mock-%realversion.tar.gz
Requires: python py2-six py2-pbr py2-funcsigs
BuildRequires: py2-setuptools

%prep
%setup -n mock-%realversion

%build
python setup.py build

%install
python setup.py install --prefix=%i --single-version-externally-managed --record=/dev/null
