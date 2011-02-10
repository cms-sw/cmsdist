### RPM external py2-scipy 0.8.0
## INITENV +PATH PYTHONPATH %i/lib/python$(echo $PYTHON_VERSION | cut -d. -f 1,2)/site-packages
%define downloadn scipy
Source: http://switch.dl.sourceforge.net/sourceforge/%downloadn/%downloadn-%{realversion}.tar.gz
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
python setup.py -h
python setup.py config_fc --fcompiler=gfortran config_cc install --prefix=%i 
perl -p -i -e "s|^#!.*python(.*)|#!/usr/bin/env python$1|" `grep -r -e "#\!.*python" %i | cut -d: -f1`

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/py2-scipy.xml
<tool name="py2-scipy" version="%v">
<client>
<environment name="PY2SHIPY_BASE" default="%i"/>
</client>
<runtime name="PYTHONPATH" value="$PY2SHIPY_BASE/lib/python2.6/site-packages" type="path"/>
</tool>
EOF_TOOLFILE
