### RPM external py2-numpy 1.11.1
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}
Source: https://github.com/numpy/numpy/releases/download/v%{realversion}/numpy-%{realversion}.tar.gz
Requires: python py2-setuptools zlib OpenBLAS
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
EOF

mkdir -p %i/${PYTHON_LIB_SITE_PACKAGES}

python setup.py build  %{makeprocesses} --fcompiler=gnu95
PYTHONPATH=%i/${PYTHON_LIB_SITE_PACKAGES}:$PYTHONPATH python setup.py install --prefix=%i
sed -ideleteme 's|#!.*/bin/python|#!/usr/bin/env python|' \
  %{i}/bin/f2py \
  %{i}/lib/python*/site-packages/numpy-*/EGG-INFO/scripts/f2py \
  %{i}/lib/python*/site-packages/numpy-*/numpy/core/tests/test_arrayprint.py \
  %{i}/lib/python*/site-packages/numpy-*/numpy/distutils/from_template.py \
  %{i}/lib/python*/site-packages/numpy-*/numpy/distutils/conv_template.py
  
find %{i} -name '*deleteme' -delete
