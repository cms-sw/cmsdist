### RPM external py2-dxr 2.0
## INITENV +PATH PYTHONPATH %i/$PYTHON_LIB_SITE_PACKAGES
Requires: python zlib py2-setuptools py2-futures py2-jinja py2-markupsafe py2-ordereddict py2-parsimonious py2-pysqlite llvm sqlite
%define isdarwin %(case %{cmsos} in (osx*) echo 1 ;; (*) echo 0 ;; esac)
%define dxrCommit ac2bda0d
%define branch master

Source0: git+https://github.com/mozilla/dxr.git?obj=%{branch}/%{dxrCommit}&export=dxr-%{dxrCommit}&module=dxr-%dxrCommit&output=/dxr-%{dxrCommit}.tgz
%define keep_archives true

%prep
%setup -T -b0 -n dxr-%dxrCommit

%build
python setup.py build

%install
python setup.py install --prefix=%i --single-version-externally-managed --record=/dev/null
perl -p -i -e "s|^#!%{cmsroot}/.*|#!/usr/bin/env python|" %{i}/bin/dxr
