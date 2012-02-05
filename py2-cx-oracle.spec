### RPM external py2-cx-oracle 5.1
## INITENV +PATH PYTHONPATH %i/$PYTHON_LIB_SITE_PACKAGES
%define online %(case %cmsplatf in (*onl_*_*) echo true;; (*) echo false;; esac)
%define downloadn cx_Oracle
Source: http://switch.dl.sourceforge.net/sourceforge/cx-oracle/%downloadn-%realversion.tar.gz
Patch: py2-cx-oracle-pingbreak

%if "%online" != "true"
Requires: oracle
%endif
Requires: oracle-env
Requires: python

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
python setup.py install --prefix=%i
find %i -name '*.egg-info' -exec rm {} \;
