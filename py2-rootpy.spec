### RPM external py2-rootpy 0.8.0
## INITENV +PATH PYTHONPATH %{i}/$PYTHON_LIB_SITE_PACKAGES
%define my_name %(echo %n | cut -f2 -d-)
Source: https://github.com/rootpy/%my_name/archive/%{realversion}.tar.gz

Requires: python root py2-matplotlib root
BuildRequires: py2-setuptools

%prep
%setup -n %{my_name}-%{realversion}

%build
python setup.py build

%install
python setup.py install --single-version-externally-managed --record=/dev/null  --prefix=%{i}
find %{i}/${PYTHON_LIB_SITE_PACKAGES} -name '*.egg-info' -print0 | xargs -0 rm -rf
perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/rootpy %{i}/bin/roosh %{i}/bin/root2hdf5
