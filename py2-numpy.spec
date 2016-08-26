### RPM external py2-numpy 1.11.1
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}
Source: https://pypi.python.org/packages/e0/4c/515d7c4ac424ff38cc919f7099bf293dd064ba9a600e1e3835b3edefdb18/numpy-1.11.1.tar.gz
Requires: python py2-setuptools zlib lapack

%prep
%setup -n numpy-%realversion

%build
%install
case %cmsos in
  osx*) SONAME=dylib ;;
  *) SONAME=so ;;
esac

export LAPACK_ROOT
export LAPACK=$LAPACK_ROOT/lib/liblapack.$SONAME
export BLAS=$LAPACK_ROOT/lib/libblas.$SONAME
mkdir -p %i/$PYTHON_LIB_SITE_PACKAGES

python setup.py build --fcompiler=gnu95
PYTHONPATH=%i/$PYTHON_LIB_SITE_PACKAGES:$PYTHONPATH python setup.py install --prefix=%i
rm -rf %i/lib/python*/site-packages/numpy-*/EGG-INFO
sed -i -e 's|^#!%{cmsroot}/.*|#!/usr/bin/env python|' %i/bin/f2py

