### RPM external py2-pyopenssl 0.7
## INITENV +PATH PYTHONPATH %{i}/lib/python`echo $PYTHON_VERSION | cut -f1,2 -d.`/site-packages
## INITENV +PATH PATH %{i}/bin

Source: http://downloads.sourceforge.net/pyopenssl/pyOpenSSL-%realversion.tar.gz
Requires: python openssl

%prep
%setup -n pyOpenSSL-%realversion

%build
CFLAGS="-I$OPENSSL_ROOT/include -I$OPENSSL_ROOT/include/openssl" LDFLAGS="-L$OPENSSL_ROOT/lib" \
python setup.py build 

%install
python setup.py install --prefix=%i
