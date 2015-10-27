### RPM external py2-funcsigs 0.4
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}

Source0: https://pypi.python.org/packages/source/f/funcsigs/funcsigs-%{realversion}.tar.gz
Requires: python
BuildRequires: py2-setuptools

%prep
%setup -n funcsigs-%{realversion}

%build
python setup.py build

%install
python setup.py install --prefix=%i --single-version-externally-managed --record=/dev/null