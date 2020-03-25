### RPM external py2-cx-oracle 5.2.1
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}
%define downloadn cx_Oracle

Source: https://pypi.python.org/packages/source/c/cx_Oracle/cx_Oracle-%realversion.tar.gz
Patch: py2-cx-oracle-pingbreak

Requires: python oracle oracle-env

%prep
%setup -n %downloadn-%realversion
%patch -p1

cat >> setup.cfg <<- EOF
[build_ext]
include_dirs = $ORACLE_ROOT/include
library_dirs = $ORACLE_ROOT/lib
EOF

%build
python setup.py build

%install
mkdir -p %i/$PYTHON_LIB_SITE_PACKAGES
PYTHONPATH=%i/$PYTHON_LIB_SITE_PACKAGES:$PYTHONPATH \
python setup.py install --prefix=%i
find %i -name '*.egg-info' -exec rm {} \;
