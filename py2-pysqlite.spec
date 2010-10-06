### RPM external py2-pysqlite 2.4.0
## INITENV +PATH PYTHONPATH %i/lib/python`echo $PYTHON_VERSION | cut -f1,2 -d.`/site-packages
%define distname pysqlite-%realversion
%define distmaindir %(echo %realversion | cut -d. -f1,2)
Source: http://cmsrep.cern.ch/cmssw/pysqlite-mirror/%{distname}.tar.gz
Requires: python sqlite

%prep
%setup -n %{distname}

cat >> setup.cfg <<- EOF
[build_ext]
include_dirs = $SQLITE_ROOT/include
library_dirs = $SQLITE_ROOT/lib
EOF

%build
python setup.py build

%install
python setup.py install --prefix=%i
egrep -r -l '^#!.*python' %i | xargs perl -p -i -e 's{^#!.*python.*}{#!/usr/bin/env python}'
find %i -name '*.egg-info' -exec rm {} \;
