### RPM external py2-pip 9.0.3
## INITENV +PATH PATH %{i}/bin
## INITENV +PATH LD_LIBRARY_PATH %{i}/lib
## INITENV +PATH PYTHON27PATH %{i}/${PYTHON_LIB_SITE_PACKAGES}
%define my_name %(echo %n | cut -f2 -d-)
Source: https://github.com/pypa/pip/archive/%{realversion}.tar.gz
Requires: python py2-setuptools
#BuildRequires: 
  
%prep
%setup -n %{my_name}-%{realversion}

%build
python2 setup.py build

%install
python2 setup.py install --single-version-externally-managed --record=/dev/null  --prefix=%{i}
%{relocatePy2SitePackages}
perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/*
