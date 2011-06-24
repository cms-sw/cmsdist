### RPM external py2-matplotlib 1.0.1
## INITENV +PATH PYTHONPATH %i/$PYTHON_LIB_SITE_PACKAGES
Source: http://sourceforge.net/projects/matplotlib/files/matplotlib/matplotlib-%{realversion}/matplotlib-%{realversion}.tar.gz

Requires: py2-numpy 
Requires: zlib
Requires: libpng
%prep
%setup -n matplotlib-%{realversion}

cat >> setup.cfg <<- EOF
[build_ext]
include_dirs = $LIBPNG_ROOT/include:$ZLIB_ROOT/include:/usr/X11R6/include:/usr/X11R6/include/freetype2
library_dirs = $LIBPNG_ROOT/lib:$ZLIB_ROOT/lib:/usr/X11/lib
EOF

%build
python setup.py build 

%install
python -c 'import numpy'
python setup.py install --prefix=%i
find %i -name '*.egg-info' -exec rm {} \;
