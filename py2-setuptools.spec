### RPM external py2-setuptools 41.2.0
## INITENV +PATH PYTHON27PATH %{i}/${PYTHON_LIB_SITE_PACKAGES}
## INITENV +PATH PYTHON3PATH %{i}/${PYTHON3_LIB_SITE_PACKAGES}

Source: https://github.com/pypa/setuptools/archive/v%{realversion}.tar.gz

Requires: python python3

%prep
%setup -n setuptools-%{realversion}

%build
python bootstrap.py
python3 setup.py build
python setup.py build

%install
python3 setup.py install --single-version-externally-managed --record=/dev/null --skip-build --prefix=%{i}
python setup.py install --single-version-externally-managed --record=/dev/null --skip-build --prefix=%{i}
sed -i 's|#!.*/bin/python|#!/usr/bin/env python|' %{i}/bin/easy_install*
sed -i 's|#!.*python.*|#!/usr/bin/env python3|' \
 %{i}/lib/python3.6/site-packages/setuptools/command/easy_install.py \
 %{i}/lib/python3.6/site-packages/pkg_resources/_vendor/appdirs.py
