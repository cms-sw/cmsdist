### RPM external py2-nose 1.3.7
## INITENV +PATH PYTHONPATH %{i}/$PYTHON_LIB_SITE_PACKAGES
%define my_name %(echo %n | cut -f2 -d-)
Source: https://pypi.python.org/packages/58/a5/0dc93c3ec33f4e281849523a5a913fa1eea9a3068acfa754d44d88107a44/nose-%{realversion}.tar.gz 
Requires: python
BuildRequires: py2-setuptools

%prep
%setup -n %{my_name}-%{realversion}

%build
python setup.py build

%install
python setup.py install --single-version-externally-managed --record=/dev/null --skip-build --prefix=%{i}
perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/nosetests-2.7 %{i}/bin/nosetests

