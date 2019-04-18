%ifarch aarch64
### RPM external py2-numpy 1.15.1
%else 
### RPM external py2-numpy 1.16.2
%endif
## INITENV +PATH PYTHON27PATH %i/${PYTHON_LIB_SITE_PACKAGES}
## INITENV +PATH PYTHON3PATH %i/${PYTHON3_LIB_SITE_PACKAGES}
## INITENV SET PY2_NUMPY_REAL_VERSION %{realversion}


Source: https://github.com/numpy/numpy/releases/download/v%{realversion}/numpy-%{realversion}.tar.gz
Requires: zlib OpenBLAS python python3
#py2-setuptools
BuildRequires: py2-pip

%define pythonver %(echo %{allpkgreqs} | tr ' ' '\\n' | grep ^external/python/ | cut -d/ -f3 | cut -d. -f 1,2)
%define numpyArch %(uname -m)


%prep
%setup -n numpy-%realversion

%build
%install
case %cmsos in
  osx*) SONAME=dylib ;;
  *) SONAME=so ;;
esac

cat > site.cfg <<EOF
[default]
include_dirs = $OPENBLAS_ROOT/include
library_dirs = $OPENBLAS_ROOT/lib
[openblas]
openblas_libs = openblas
library_dirs = $OPENBLAS_ROOT/lib
[lapack]
lapack_libs = openblas
library_dirs = $OPENBLAS_ROOT/lib
[atlas]
atlas_libs = openblas
atlas_dirs = $OPENBLAS_ROOT/lib
[build]
fcompiler=gnu95
EOF

mkdir -p %i/${PYTHON_LIB_SITE_PACKAGES}

export PYTHONUSERBASE=%i
pip2 install . --user 
pip3 install . --user 

perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/*

#afaik, this functionality is not needed - but keep it for now.
mkdir %{i}/c-api
PYTHONV=$(echo $PYTHON_VERSION | cut -f1,2 -d.)
OSARCH=$(uname -m)
[ -d  %{i}/${PYTHON_LIB_SITE_PACKAGES}/numpy/core ] || exit 1
ln -s   ../${PYTHON_LIB_SITE_PACKAGES}/numpy/core %{i}/c-api/core


%post
%{relocateConfig}lib/python*/site-packages/numpy/__config__.py
%{relocateConfig}lib/python*/site-packages/numpy/distutils/__config__.py
%{relocateConfig}lib/python*/site-packages/numpy/distutils/site.cfg

