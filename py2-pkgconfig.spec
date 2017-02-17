### RPM external py2-pkgconfig 1.1.0
## INITENV +PATH PYTHONPATH %{i}/$PYTHON_LIB_SITE_PACKAGES

Source: https://pypi.python.org/packages/87/35/4af9634270c00e3411cf951b7e0ea796c262922357cfc7609a86d31f072b/pkgconfig-1.1.0.tar.gz
BuildRequires: py2-setuptools
Requires: python py2-nose

%prep
%setup -n pkgconfig-%{realversion}

%build
python setup.py build

%install
python setup.py install --single-version-externally-managed --record=/dev/null --skip-build --prefix=%{i}

