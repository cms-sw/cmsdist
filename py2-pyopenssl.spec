### RPM external py2-pyopenssl 0.7
## INITENV +PATH PYTHONPATH %i/lib/python`echo $PYTHON_VERSION | cut -f1,2 -d.`/site-packages

Source: http://downloads.sourceforge.net/pyopenssl/pyOpenSSL-%realversion.tar.gz
Requires: python openssl

%prep
%setup -n pyOpenSSL-%realversion

cat >> setup.cfg <<- EOF
[build_ext]
include_dirs = $OPENSSL_ROOT/include
library_dirs = $OPENSSL_ROOT/lib
EOF

%build
python setup.py build 

%install
python setup.py install --prefix=%i
egrep -r -l '^#!.*python' %i | xargs perl -p -i -e 's{^#!.*python.*}{#!/usr/bin/env python}'
find %i -name '*.egg-info' -exec rm {} \;

