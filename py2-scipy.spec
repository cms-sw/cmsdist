### RPM external py2-scipy 0.16.1
## INITENV +PATH PYTHONPATH %i/lib/python$(echo $PYTHON_VERSION | cut -d. -f 1,2)/site-packages
%define downloadn scipy
Source: http://vorboss.dl.sourceforge.net/project/%downloadn/%downloadn/%{realversion}/%downloadn-%{realversion}.tar.gz
Requires: python
Requires: py2-numpy
#Requires: atlas
Requires: lapack
%prep
%setup -n %downloadn-%{realversion}

cat > site.cfg <<EOF
[blas]
include_dirs = $LAPACK_ROOT/include
library_dirs = $LAPACK_ROOT/lib
blas_libs = blas
[lapack]
include_dirs = $LAPACK_ROOT/include
library_dirs = $LAPACK_ROOT/lib
lapack_libs = lapack
EOF

%build
%install
case %cmsos in
  osx*) SONAME=dylib ;;
  *) SONAME=so ;;
esac

LAPACK=$LAPACK_ROOT/lib/liblapack.$SONAME
BLAS=$LAPACK_ROOT/lib/libblas.$SONAME
ATLAS=None

LAPACK=$LAPACK BLAS=$BLAS ATLAS=$ATLAS python setup.py config_fc --fcompiler=gfortran config_cc install --prefix=%{i}
perl -p -i -e "s|^#!.*python(.*)|#!/usr/bin/env python$1|" `grep -r -e "#\!.*python" %i | cut -d: -f1`

