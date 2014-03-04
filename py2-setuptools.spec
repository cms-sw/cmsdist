### RPM external py2-setuptools 2.1
## INITENV +PATH PYTHONPATH %{i}/$PYTHON_LIB_SITE_PACKAGES

Source: https://pypi.python.org/packages/source/s/setuptools/setuptools-%{realversion}.tar.gz
Requires: python

%prep
%setup -n setuptools-%{realversion}

%build
python setup.py build

%install
python setup.py install --single-version-externally-managed --record=/dev/null --skip-build --prefix=%{i}
sed -ideleteme 's|#!.*/bin/python|#!/usr/bin/env python|' %{i}/bin/easy_install*
rm -f %{i}/bin/*deleteme
