### RPM external py2-dxr 1.0
## INITENV +PATH PYTHONPATH %i/$PYTHON_LIB_SITE_PACKAGES
BuildRequires: llvm sqlite
Requires: python py2-setuptools py2-futures py2-jinja py2-markupsafe py2-ordereddict py2-parsimonious

%define dxrCommit 6ea764102a
%define triliteCommit e64a2a1 
%define re2Version 20140304
%define branch master

Source0: git+https://github.com/mozilla/dxr.git?obj=%{branch}/%{dxrCommit}&export=dxr-%{dxrCommit}&module=dxr-%dxrCommit&output=/dxr-%{dxrCommit}.tgz
Source1: git+https://github.com/jonasfj/trilite.git?obj=%{branch}/%{triliteCommit}&export=trilite-%{triliteCommit}&module=trilite-%triliteCommit&output=/trilite-%{triliteCommit}.tgz
Source2: https://re2.googlecode.com/files/re2-%re2Version.tgz
Patch0: py2-dxr
Patch1: trilite
%define keep_archives true

%prep
%setup -T -b0 -n dxr-%dxrCommit
%setup -T -D -a1 -c -n dxr-%dxrCommit
%setup -T -D -a2 -n dxr-%dxrCommit/trilite-%triliteCommit
%patch -P 1 -p0
cd ..
%patch -P 0 -p1
mv trilite-%triliteCommit/* trilite
%setup -T -D -n dxr-%dxrCommit


%build
export SQLITE_ROOT; make build-plugin-clang build-plugin-pygmentize;cd  trilite; make release; cd re2; make ; cd ../../; python setup.py build


%install
mkdir %i/lib
cp -p trilite/libtrilite.so %i/lib
cp -p trilite/re2/obj/libre2.a %i/lib
python setup.py install --prefix=%i  --single-version-externally-managed --record=/dev/null
perl -p -i -e "s|^#!%{cmsroot}/.*|#!/usr/bin/env python|" %{i}/bin/*.py
