### RPM external py2-scipy 0.15.0
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}
Source: http://downloads.sourceforge.net/project/scipy/scipy/%realversion/scipy-%realversion.tar.gz
Requires: python py2-numpy zlib lapack

%prep
%setup -n scipy-%realversion

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
PYTHONPATH=%i/$PYTHON_LIB_SITE_PACKAGES:$PYTHONPATH \
python setup.py install --prefix=%i
find %i -name '*.egg-info' -exec rm {} \;
find %i/$PYTHON_LIB_SITE_PACKAGES -name '*.py' -exec chmod a-x {} \;
perl -p -i -e 's{^#!.*/python}{#!/usr/bin/env python}' %i/bin/*
