### RPM external py2-setuptools 44.1.1
## INITENV +PATH PYTHON27PATH %{i}/${PYTHON_LIB_SITE_PACKAGES}

Source: https://github.com/pypa/setuptools/archive/v%{realversion}.tar.gz

Requires: python
# python3

%prep
%setup -n setuptools-%{realversion}

%build
which python
python bootstrap.py
python setup.py build

%install
python setup.py install --single-version-externally-managed --record=/dev/null --skip-build --prefix=%{i}
sed -i 's|#!.*/bin/python|#!/usr/bin/env python|' %{i}/bin/easy_install*
