### RPM external py2-matplotlib 1.4.3
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}
Source: http://sourceforge.net/projects/matplotlib/files/matplotlib/matplotlib-%{realversion}/matplotlib-%{realversion}.tar.gz
Requires: py2-pytz py2-numpy py2-python-dateutil zlib libpng freetype py2-pyparsing py2-six
BuildRequires: py2-setuptools

%prep
%setup -n matplotlib-%{realversion}

cat >> setup.cfg <<- EOF
[directories]
basedirlist = ${FREETYPE_ROOT},${LIBPNG_ROOT},${ZLIB_ROOT},${PY2_NUMPY_ROOT},${PY2_PYTZ_ROOT},${PY2_SIX}

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
python setup.py install --prefix=%i  --single-version-externally-managed --record=/dev/null

# No need for test files
rm -rf %i/$PYTHON_LIB_SITE_PACKAGES/matplotlib/tests
