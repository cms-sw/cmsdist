### RPM external py2-matplotlib 1.2.1
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}
Source: http://sourceforge.net/projects/matplotlib/files/matplotlib/matplotlib-%{realversion}/matplotlib-%{realversion}.tar.gz
Requires: py2-pytz py2-numpy py2-python-dateutil zlib libpng freetype py2-pyparsing
BuildRequires: py2-setuptools

%prep
%setup -n matplotlib-%{realversion}

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

%build
python setup.py build

%install
python setup.py install --prefix=%i # --single-version-externally-managed --record=/dev/null
find %i -name '*.egg-info' -exec rm {} \;

# No need for test files
rm -rf %i/$PYTHON_LIB_SITE_PACKAGES/matplotlib/tests
