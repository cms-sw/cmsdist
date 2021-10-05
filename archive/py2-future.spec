### RPM external py2-future 0.18.2
## INITENV +PATH PATH %{i}/bin
## INITENV +PATH LD_LIBRARY_PATH %{i}/lib
## INITENV +PATH PYTHON27PATH %{i}/${PYTHON_LIB_SITE_PACKAGES}

%define my_name %(echo %n | cut -f2 -d-)
Source: https://files.pythonhosted.org/packages/45/0b/38b06fd9b92dc2b68d58b75f900e97884c45bedd2ff83203d933cf5851c9/future-0.18.2.tar.gz
Requires: python

%prep
%setup -n %{my_name}-%{realversion}

%build
python setup.py build

%install
python setup.py install  --prefix=%{i}
%{relocatePy2SitePackages}
perl -p -i -e "s|^#!.*python.*|#!/usr/bin/env python|" %{i}/bin/*
