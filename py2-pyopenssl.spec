### RPM external py2-pyopenssl 0.7
## INITENV +PATH PYTHONPATH %i/$PYTHON_LIB_SITE_PACKAGES

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
find %i -name '*.egg-info' -exec rm {} \;
