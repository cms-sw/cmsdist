### RPM external py2-cx-oracle 5.0.1
## INITENV +PATH PYTHONPATH %i/lib/python`echo $PYTHON_VERSION | cut -d. -f 1,2`/site-packages
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
python setup.py install --prefix=%i
egrep -r -l '^#!.*python' %i | xargs perl -p -i -e 's{^#!.*python.*}{#!/usr/bin/env python}'
find %i -name '*.egg-info' -exec rm {} \;

