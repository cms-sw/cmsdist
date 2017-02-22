### RPM external gosam 2.0.4-12f4de9
Source: http://www.hepforge.org/archive/gosam/gosam-%{realversion}.tar.gz



%if "%{?cms_cxx:set}" != "set"
%define cms_cxx g++
%endif


%prep
%setup -q -n gosam


%build
CXX="$(which %{cms_cxx}) -fPIC"
CC="$(which gcc) -fPIC"
FC="$(which gfortran)"
PLATF_CONF_OPTS="--enable-shared --disable-static"
export PYTHONPATH=${CYTHON_ROOT}/${PYTHON_LIB_SITE_PACKAGES}


chmod 0755 ./gosam_installer.py
./gosam_installer.py -b -v --prefix=%{i}


%install
perl -p -i -e "s|^#!.*python|#!/usr/bin/env python$1|" $(grep -r -e "^#\!.*python.*" %i | cut -d: -f1)
find %{i}/lib -name '*.la' -exec rm -f {} \;


%post

