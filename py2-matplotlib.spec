### RPM external py2-matplotlib 0.98.5.3
## INITENV +PATH PYTHONPATH %i/lib/python`echo $PYTHON_VERSION | cut -d. -f 1,2`/site-packages
%define downloadn matplotlib
Source: http://switch.dl.sourceforge.net/sourceforge/%downloadn/%downloadn-%realversion.tar.gz
Requires: python
Requires: zlib
# Requires: agg
# Requires: cairo
Requires: py2-numpy 
# py2-numpy is now built using its internal lapack_lite.
# uncomment if otherwise.
# Requires: atlas lapack
Requires: libpng
# Requires: freetype

%prep
%setup -n %downloadn-%realversion
cat >> setup.cfg <<- EOF
[build_ext]
include_dirs = $LIBPNG_ROOT/include:$ZLIB_ROOT/include
library_dirs = $LIBPNG_ROOT/lib:$ZLIB_ROOT/lib
EOF

%build
python setup.py build

%install
python -c 'import numpy'
python setup.py install --prefix=%i
egrep -r -l '^#!.*python' %i | xargs perl -p -i -e 's{^#!.*python.*}{#!/usr/bin/env python}'
find %i -name '*.egg-info' -exec rm {} \;

