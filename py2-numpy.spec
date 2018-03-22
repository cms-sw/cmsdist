### RPM external py2-numpy 1.14.1
## INITENV +PATH PYTHON27PATH %i/${PYTHON_LIB_SITE_PACKAGES}
## INITENV SET PY2_NUMPY_REAL_VERSION %{realversion}

Source: https://github.com/numpy/numpy/releases/download/v%{realversion}/numpy-%{realversion}.tar.gz
Requires: python py2-setuptools zlib OpenBLAS

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
EOF

mkdir -p %i/${PYTHON_LIB_SITE_PACKAGES}

python setup.py build  %{makeprocesses} --fcompiler=gnu95
PYTHON27PATH=%i/${PYTHON_LIB_SITE_PACKAGES}:$PYTHON27PATH python setup.py install --prefix=%i
sed -ideleteme 's|#!.*/bin/python|#!/usr/bin/env python|' \
  %{i}/bin/f2py \
  %{i}/lib/python*/site-packages/numpy-*/EGG-INFO/scripts/f2py \
  %{i}/lib/python*/site-packages/numpy-*/numpy/core/tests/test_arrayprint.py \
  %{i}/lib/python*/site-packages/numpy-*/numpy/distutils/from_template.py \
  %{i}/lib/python*/site-packages/numpy-*/numpy/distutils/conv_template.py

  
find %{i} -name '*deleteme' -delete
mkdir %{i}/c-api
PYTHONV=$(echo $PYTHON_VERSION | cut -f1,2 -d.)
OSARCH=$(uname -m)
[ -d  %{i}/${PYTHON_LIB_SITE_PACKAGES}/numpy-%{realversion}-py${PYTHONV}-linux-$OSARCH.egg/numpy/core ] || exit 1
ln -s   ../${PYTHON_LIB_SITE_PACKAGES}/numpy-%{realversion}-py${PYTHONV}-linux-$OSARCH.egg/numpy/core %{i}/c-api/core
%post
%{relocateConfig}lib/python*/site-packages/numpy-*.egg/numpy/__config__.py
%{relocateConfig}lib/python*/site-packages/numpy-*.egg/numpy/distutils/__config__.py
%{relocateConfig}lib/python*/site-packages/numpy-*.egg/numpy/distutils/site.cfg
