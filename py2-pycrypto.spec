### RPM external py2-pycrypto 2.0.1 
## INITENV +PATH PYTHONPATH %i/lib/python`echo $PYTHON_VERSION | cut -d. -f 1,2`/site-packages

%define downloadn pycrypto
Requires: python gmp
Source: http://www.amk.ca/files/python/crypto/%downloadn-%realversion.tar.gz 

%prep
%setup -n %downloadn-%realversion

cat >> setup.cfg <<- EOF
[build_ext]
include_dirs = $GMP_ROOT/include
library_dirs = $GMP_ROOT/lib
EOF

%build
python setup.py build

%install
python setup.py install --prefix=%i
egrep -r -l '^#!.*python' %i | xargs perl -p -i -e 's{^#!.*python.*}{#!/usr/bin/env python}'
find %i -name '*.egg-info' -exec rm {} \;
