### RPM external gosam 2.0
## INITENV +PATH LD_LIBRARY_PATH %{i}/lib
## INITENV +PATH DYLD_LIBRARY_PATH %{i}/lib

# Download from official webpage
Source: http://gosam.hepforge.org/gosam_installer.py

Requires: python cython

%define keep_archives false

%if "%{?cms_cxx:set}" != "set"
%define cms_cxx c++
%endif

%prep
%setup -T  -c -D


%build
CXX="$(which %{cms_cxx}) -fPIC"
CC="$(which gcc) -fPIC"
PLATF_CONF_OPTS="--enable-shared --disable-static"
PYTHONPATH=${CYTHON_ROOT}/${PYTHON_LIB_SITE_PACKAGES}


wget http://gosam.hepforge.org/gosam_installer.py
chmod 0755 ./gosam_installer.py
./gosam_installer.py -b -v --prefix=%{i}


%install
perl -p -i -e "s|^#!.*python|#!/usr/bin/env python$1|" $(grep -r -e "^#\!.*python.*" %i | cut -d: -f1)
find %{i}/lib -name '*.la' -exec rm -f {} \;

%post
