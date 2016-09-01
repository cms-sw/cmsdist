### RPM external py2-pep8 1.7.0
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}
Source: https://pypi.python.org/packages/source/p/pep8/pep8-%realversion.tar.gz
Requires: python
BuildRequires: py2-setuptools

%prep
%setup -n pep8-%realversion

%build
python setup.py build

%install
python setup.py install --prefix=%i --single-version-externally-managed --record=/dev/null
