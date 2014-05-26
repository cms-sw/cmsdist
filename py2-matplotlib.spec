### RPM external py2-matplotlib 1.0.1
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}
Source: http://sourceforge.net/projects/matplotlib/files/matplotlib/matplotlib-%{realversion}/matplotlib-%{realversion}.tar.gz
Requires: py2-pytz py2-numpy py2-python-dateutil zlib libpng freetype

%prep
%setup -n matplotlib-%{realversion}
perl -p -i -e '/^import sys/ && print "for v in basedir.values(): v[:] = []\n"' setupext.py

cat >> setup.cfg <<- EOF
[build_ext]
include_dirs = $FREETYPE_ROOT/include/freetype2:$FREETYPE_ROOT/include:$LIBPNG_ROOT/include:$ZLIB_ROOT/include:/usr/X11R6/include:/usr/X11R6/include/freetype2
library_dirs = $FREETYPE_ROOT/lib:$LIBPNG_ROOT/lib:$ZLIB_ROOT/lib:/usr/X11/lib

[gui_support]
gtk = False
gtkagg = False
tkagg = False
wxagg = False
macosx = False
EOF

mkdir no-pkg-config
(echo '#!/bin/sh'; echo 'exit 1') > no-pkg-config/pkg-config
chmod +x no-pkg-config/pkg-config

%build
export MPLCONFIGDIR=$PWD/no-pkg-config
PATH=$PWD/no-pkg-config:$PATH \
python setup.py build 

%install
python -c 'import numpy'
PATH=$PWD/no-pkg-config:$PATH \
# Notice that the install procedure will try to write in $HOME/.matplotlib by
# default!!! This should work around the problem and have it write config
# in a scratch area.
export MPLCONFIGDIR=$PWD/no-pkg-config

python setup.py install --prefix=%i
find %i -name '*.egg-info' -exec rm {} \;

# No need for test files
rm -rf %i/$PYTHON_LIB_SITE_PACKAGES/matplotlib/tests
