### RPM external py3-pip 23.1.1
## INITENV +PATH PATH %{i}/bin
## INITENV +PATH LD_LIBRARY_PATH %{i}/lib
## INITENV +PATH PYTHON3PATH %{i}/${PYTHON3_LIB_SITE_PACKAGES}
%define my_name %(echo %n | cut -f2 -d-)
Source: https://github.com/pypa/pip/archive/%{realversion}.tar.gz
Requires: python3 py3-setuptools

%prep
%setup -n %{my_name}-%{realversion}

%build
python3 setup.py build

%install
python3 setup.py install --single-version-externally-managed --record=/dev/null  --prefix=%{i}
%{relocatePy3SitePackages}
perl -p -i -e "s|^#!.*python.*|#!/usr/bin/env python3|" %{i}/bin/*
rm -f %{i}/bin/pip
