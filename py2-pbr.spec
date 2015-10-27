### RPM external py2-pbr 1.8.1
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}

Source0: https://pypi.python.org/packages/source/p/pbr/pbr-%{realversion}.tar.gz
Requires: python
BuildRequires: py2-setuptools

%prep
%setup -n pbr-%{realversion}

%build
python setup.py build

%install
python setup.py install --prefix=%i --single-version-externally-managed --record=/dev/null
