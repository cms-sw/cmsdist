### RPM external py3-pip 25.1.1
## INITENV +PATH PATH %{i}/bin
## INITENV +PATH LD_LIBRARY_PATH %{i}/lib
## INITENV +PATH PYTHON3PATH %{i}/${PYTHON3_LIB_SITE_PACKAGES}
%define my_name %(echo %n | cut -f2 -d-)
Source: https://raw.githubusercontent.com/pypa/get-pip/refs/tags/%{realversion}/public/get-pip.py
Requires: python3 py3-setuptools

%prep

%build
python3 %{_sourcedir}/get-pip.py  --no-setuptools --no-wheel pip==%{realversion} --prefix=%{i}

%install
%{relocatePy3SitePackages}
rm -f %{i}/bin/pip
perl -p -i -e "s|^#!.*python.*|#!/usr/bin/env python3|" %{i}/bin/pip3*
perl -p -i -e "s| %{cmsroot}/.*/python3 | python3 |" %{i}/bin/pip3*
