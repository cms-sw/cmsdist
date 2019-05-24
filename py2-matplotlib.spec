### RPM external py2-matplotlib 2.2.4
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}

Source: https://github.com/matplotlib/matplotlib/archive/v%{realversion}.tar.gz
Requires: py2-pytz py2-numpy py2-python-dateutil zlib libpng freetype py2-pyparsing py2-six py2-cycler py2-subprocess32 py2-kiwisolver
#Requires: py2-backports
BuildRequires: py2-pip

%prep
%setup -n matplotlib-%{realversion}

cat >> setup.cfg <<- EOF
[directories]
basedirlist = ${FREETYPE_ROOT}:${LIBPNG_ROOT}:${ZLIB_ROOT}:${PY2_NUMPY_ROOT}:${PY2_PYTZ_ROOT}:${PY2_SIX}

[gui_support]
gtk = False
gtkagg = False
tkagg = True
wxagg = False
macosx = False
EOF

mkdir no-pkg-config
(echo '#!/bin/sh'; echo 'exit 1') > no-pkg-config/pkg-config
chmod +x no-pkg-config/pkg-config

%build
#python setup.py build

%install
export CPLUS_INCLUDE_PATH=${FREETYPE_ROOT}/include/freetype2:${LIBPNG_ROOT}/include/libpng16
export MPLCONFIGDIR=$PWD/no-pkg-config
PATH=$PWD/no-pkg-config:$PATH \
export CPLUS_INCLUDE_PATH=${FREETYPE_ROOT}/include/freetype2:${LIBPNG_ROOT}/include/libpng16
export PYTHONUSERBASE=%i
pip install . --user

#python setup.py install --prefix=%i  --single-version-externally-managed --record=/dev/null

# No need for test files
rm -rf %i/${PYTHON_LIB_SITE_PACKAGES}/matplotlib/tests
