### RPM external py2-retry 0.9.1
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}
Source: https://pypi.python.org/packages/source/r/retry/retry-%realversion.tar.gz
Requires: python
BuildRequires: py2-setuptools

%prep
%setup -n retry-%realversion

%build
python setup.py build

%install
python setup.py install --prefix=%i --single-version-externally-managed --record=/dev/null