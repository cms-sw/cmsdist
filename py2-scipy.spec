### RPM external py2-scipy 0.8.0
## INITENV +PATH PYTHONPATH %i/lib/python$(echo $PYTHON_VERSION | cut -d. -f 1,2)/site-packages
%define downloadn scipy
Source: http://switch.dl.sourceforge.net/sourceforge/%downloadn/%downloadn-%{realversion}.tar.gz
Patch0: py2-scipy-0.8.0-fix-python27-build-rev-6645
Requires: python
Requires: py2-numpy
#Requires: atlas
Requires: lapack
%prep
%setup -n %downloadn-%{realversion}
%patch0 -p1


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

export ATLAS=None
export OPENBLAS=None

mkdir -p %{i}/${PYTHON_LIB_SITE_PACKAGES}
export PYTHONPATH=%{i}/${PYTHON_LIB_SITE_PACKAGES}:${PYTHONPATH}

python setup.py config_fc --fcompiler=gfortran config_cc install --prefix=%i 
perl -p -i -e "s|^#!.*python(.*)|#!/usr/bin/env python$1|" `grep -r -e "#\!.*python" %i | cut -d: -f1`

