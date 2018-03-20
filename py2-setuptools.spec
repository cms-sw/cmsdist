### RPM external py2-setuptools 28.3.0
## INITENV +PATH PYTHON27PATH %{i}/${PYTHON_LIB_SITE_PACKAGES}

Source: https://pypi.python.org/packages/6b/dd/a7de8caeeffab76bacf56972b3f090c12e0ae6932245abbce706690a6436/setuptools-28.3.0.tar.gz
Requires: python

%prep
%setup -n setuptools-%{realversion}

%build
python setup.py build

%install
python setup.py install --single-version-externally-managed --record=/dev/null --skip-build --prefix=%{i}
sed -ideleteme 's|#!.*/bin/python|#!/usr/bin/env python|' %{i}/bin/easy_install*
rm -f %{i}/bin/*deleteme
