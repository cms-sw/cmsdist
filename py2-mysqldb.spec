### RPM external py2-mysqldb 1.2.4b4
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}
%define downloadn MySQL-python

Source: https://pypi.python.org/packages/source/M/MySQL-python/%downloadn-%realversion.tar.gz
Requires: python mariadb openssl
Patch0: py2-mysqldb-setup

%prep
%setup -n %downloadn-%realversion
%patch0 -p0
cat >> setup.cfg <<- EOF
include_dirs = $MARIADB_ROOT/include:$OPENSSL_ROOT/include
library_dirs = $MARIADB_ROOT/lib:$OPENSSL_ROOT/lib
EOF

%build
python setup.py build

%install
python setup.py install --prefix=%i
find %i -name '*.egg-info' -exec rm {} \;
