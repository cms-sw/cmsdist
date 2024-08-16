### RPM external py3-setuptools 72.2.0
## INITENV +PATH PYTHON3PATH %{i}/${PYTHON3_LIB_SITE_PACKAGES}

Source: https://github.com/pypa/setuptools/archive/v%{realversion}.tar.gz

Requires: python3

%prep
%setup -n setuptools-%{realversion}

%build
python3 setup.py build
python3 setup.py egg_info

%install
python3 setup.py install --single-version-externally-managed --record=/dev/null --skip-build --prefix=%{i}
