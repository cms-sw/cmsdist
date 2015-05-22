### RPM external py2-cx-oracle 5.1
## INITENV +PATH PYTHONPATH %i/$PYTHON_LIB_SITE_PACKAGES
%define downloadn cx_Oracle
Source: http://switch.dl.sourceforge.net/sourceforge/cx-oracle/%downloadn-%realversion.tar.gz

Requires: python oracle oracle-env

%prep
%setup -n %downloadn-%realversion

cat >> setup.cfg <<- EOF
[build_ext]
include_dirs = $ORACLE_ROOT/include
library_dirs = $ORACLE_ROOT/lib
EOF

%build
python setup.py build

%install
python setup.py install  --single-version-externally-managed --record=/dev/null --skip-build --prefix=%{i}
find %{i} -name '*.egg-info' | xargs rm -rf
