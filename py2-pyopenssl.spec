### RPM external py2-pyopensslsourceforge 0.6
%define pythonv `echo $PYTHON_VERSION | cut -d. -f 1,2`
## INITENV +PATH PYTHONPATH %{i}/lib/python%{pythonv}/site-packages
## INITENV +PATH PATH %{i}/bin

Source: http://downloads.sourceforge.net/pyopenssl/pyOpenSSL-%v.tar.gz
Requires: python openssl
%prep
%setup -n pyOpenSSL-%{v}

%build
CFLAGS="-I$OPENSSL_ROOT/include -I$OPENSSL_ROOT/include/openssl" LDFLAGS="-L$OPENSSL_ROOT/lib" \
python setup.py build 

%install
python setup.py install --prefix=%i
