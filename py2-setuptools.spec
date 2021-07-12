### RPM external py2-setuptools 40.5.0
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}

Source: https://files.pythonhosted.org/packages/26/e5/9897eee1100b166a61f91b68528cb692e8887300d9cbdaa1a349f6304b79/setuptools-%realversion.zip
Requires: python

%prep
%setup -n setuptools-%realversion

%build
python setup.py build

%install
python setup.py install --single-version-externally-managed --record=/dev/null --skip-build --prefix=%{i}
sed -ideleteme 's|#!.*/bin/python|#!/usr/bin/env python|' %{i}/bin/easy_install*
rm -f %{i}/bin/*deleteme
