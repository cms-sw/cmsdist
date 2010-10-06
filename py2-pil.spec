### RPM external py2-pil 1.1.6
## INITENV +PATH PYTHONPATH %i/lib/python`echo $PYTHON_VERSION | cut -d. -f 1,2`/site-packages
## INITENV +PATH PYTHONPATH %i/lib/python`echo $PYTHON_VERSION | cut -d. -f 1,2`/site-packages/PIL
%define downloadn Imaging
Source: http://effbot.org/downloads/%downloadn-%realversion.tar.gz
Requires: python
# Requires: zlib
# Requires: agg
# Requires: cairo
# py2-numpy is now built using its internal lapack_lite.
# uncomment if otherwise.
# Requires: atlas lapack
Requires: libpng libjpg zlib libtiff
# Requires: freetype

%prep
%setup -n %downloadn-%realversion

cat >> setup.cfg <<- EOF
[build_ext]
include_dirs = $LIBJPG_ROOT/include:$LIBTIFF_ROOT/include:$ZLIB_ROOT/include
library_dirs = $LIBJPG_ROOT/lib:$LIBTIFF_ROOT/lib:$ZLIB_ROOT/lib
EOF


%build
python setup.py build_ext -i
python selftest.py

%install
python setup.py install --prefix=%i
egrep -r -l '^#!.*python' %i | xargs perl -p -i -e 's{^#!.*python.*}{#!/usr/bin/env python}'
find %i -name '*.egg-info' -exec rm {} \;

