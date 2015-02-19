### RPM external py2-pyopenssl 0.11
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}

Source: https://launchpad.net/pyopenssl/main/%realversion/+download/pyOpenSSL-%realversion.tar.gz
Requires: python openssl

%prep
%setup -n pyOpenSSL-%realversion

cat >> setup.cfg <<CMS_EOF
[build_ext]
include_dirs = $OPENSSL_ROOT/include
library_dirs = $OPENSSL_ROOT/lib
CMS_EOF

%build
python setup.py build 

%install
python setup.py install --prefix=%i
find %i -name '*.egg-info' -exec rm {} \;
