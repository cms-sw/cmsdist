### RPM external py2-scipy 0.5.1
Requires: gcc-wrapper
## INITENV +PATH PYTHONPATH %i/lib/python$(echo $PYTHON_VERSION | cut -d. -f 1,2)/site-packages
%define downloadn scipy
Source: http://switch.dl.sourceforge.net/sourceforge/%downloadn/%downloadn-%v.tar.gz
Requires: python
Requires: py2-numpy
Requires: atlas
%prep
%setup -n %downloadn-%v

cat > site.cfg <<EOF
[atlas]
include_dirs = $ATLAS_ROOT/include
library_dirs = $ATLAS_ROOT/lib
atlas_libs = ptf77blas, ptcblas
lapack_libs = lapack_atlas
EOF

%build
## IMPORT gcc-wrapper
%install
python setup.py install --prefix=%i
perl -p -i -e "s|^#!.*python(.*)|#!/usr/bin/env python$1|" `grep -r -e "#\!.*python" %i | cut -d: -f1`
