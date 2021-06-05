### RPM external py2-dxr 1.0.x
## INITENV +PATH PYTHON27PATH %i/${PYTHON_LIB_SITE_PACKAGES}
## INITENV +PATH PYTHON3PATH %i/${PYTHON3_LIB_SITE_PACKAGES}
Requires: python python3 zlib py2-setuptools py2-pysqlite llvm sqlite py3-setuptools
Requires: py2-Jinja2 py2-parsimonious
%define dxrCommit c540b2b322d57045633d2b60c581586520082402
%define triliteCommit e64a2a1 
%define re2Version 20140304
%define branch cms/master/6ea764102a

Source0: git+https://github.com/cms-externals/dxr.git?obj=%{branch}/%{dxrCommit}&export=dxr-%{dxrCommit}&module=dxr-%dxrCommit&output=/dxr-%{dxrCommit}.tgz
Source1: git+https://github.com/jonasfj/trilite.git?obj=master/%{triliteCommit}&export=trilite-%{triliteCommit}&module=trilite-%triliteCommit&output=/trilite-%{triliteCommit}.tgz
Source2: https://re2.googlecode.com/files/re2-%re2Version.tgz
Patch0: trilite
%define keep_archives true

%prep
%setup -T -b0 -n dxr-%dxrCommit
%setup -T -D -a1 -c -n dxr-%dxrCommit
%setup -T -D -a2 -n dxr-%dxrCommit/trilite-%triliteCommit
%patch0 -p1
cd ..
mv trilite-%triliteCommit/* trilite
%setup -T -D -n dxr-%dxrCommit

%build
export SQLITE_ROOT
LDFLAGS="-L${ZLIB_ROOT}/lib" make build-plugin-clang build-plugin-pygmentize
cd trilite
make release
cd re2
make
cd ../../
python2 setup.py build
python3 setup.py build

%install
mkdir %i/lib
cp -p trilite/libtrilite.so %i/lib
cp -p trilite/re2/obj/libre2.a %i/lib
python2 setup.py install --prefix=%i  --single-version-externally-managed --record=/dev/null
python3 setup.py install --prefix=%i  --single-version-externally-managed --record=/dev/null
perl -p -i -e "s|^#!%{cmsroot}/.*|#!/usr/bin/env python|" %{i}/bin/*.py
