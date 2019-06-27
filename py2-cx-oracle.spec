### RPM external py2-cx-oracle 5.2.1
## INITENV +PATH PYTHON27PATH %{i}/${PYTHON_LIB_SITE_PACKAGES}
## INITENV +PATH PYTHON3PATH %{i}/${PYTHON3_LIB_SITE_PACKAGES}
%define downloadn cx_Oracle
Source: https://bitbucket.org/anthony_tuininga/cx_oracle/get/%{realversion}.tar.gz

Requires: python oracle

%define commit 76da8847ab83

%prep
%setup -n anthony_tuininga-cx_oracle-%{commit}

cat >> setup.cfg <<- EOF
[build_ext]
include_dirs = $ORACLE_ROOT/include
library_dirs = $ORACLE_ROOT/lib
EOF

%build
python setup.py build

%install
python setup.py install --skip-build --prefix=%{i}
find %{i} -name '*.egg-info' | xargs rm -rf
# bla bla
