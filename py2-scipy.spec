### RPM external py2-scipy 0.18.1
## INITENV +PATH PYTHONPATH %i/lib/python$(echo $PYTHON_VERSION | cut -d. -f 1,2)/site-packages
%define downloadn scipy
Source: https://github.com/%downloadn/%downloadn/archive/v%{realversion}.tar.gz
Requires: python
Requires: py2-numpy
#Requires: atlas
Requires: lapack
Requires: cython
%prep
%setup -n %downloadn-%{realversion}

cat > site.cfg <<EOF
[blas]
include_dirs = $LAPACK_ROOT/include
library_dirs = $LAPACK_ROOT/lib64
blas_libs = blas
[lapack]
include_dirs = $LAPACK_ROOT/include
library_dirs = $LAPACK_ROOT/lib64
lapack_libs = lapack
EOF

%build
%install
case %cmsos in
  osx*) SONAME=dylib ;;
  *) SONAME=so ;;
esac

LAPACK=$LAPACK_ROOT/lib64
BLAS=$LAPACK_ROOT/lib64
ATLAS=None

mkdir -p %{i}/${PYTHON_LIB_SITE_PACKAGES}
export PYTHONPATH=%{i}/${PYTHON_LIB_SITE_PACKAGES}:${PYTHONPATH}
LAPACK=$LAPACK BLAS=$BLAS ATLAS=$ATLAS python setup.py config_fc --fcompiler=gfortran config_cc install --prefix=%{i}
perl -p -i -e "s|^#!.*python(.*)|#!/usr/bin/env python$1|" `grep -r -e "#\!.*python" %i | cut -d: -f1`

