### RPM external py2-pyopenssl 0.6.900 
Requires: gcc-wrapper
%define pythonv %(echo $PYTHON_VERSION | cut -d. -f 1,2)
## INITENV +PATH PYTHONPATH %{i}/lib/python%{pythonv}/site-packages
## INITENV +PATH PATH %{i}/bin

Summary: A Python wrapper for OpenSSL
Group: Development/Libraries
Packager: Conrad Steenberg <conrad@hep.caltech.edu>
Source: http://julian.ultralight.org/clarens/devel/pyOpenSSL-%v.tar.gz
Requires: python openssl
%prep
%setup -n pyOpenSSL-%{v}

%build
## IMPORT gcc-wrapper
CFLAGS="-I$OPENSSL_ROOT/include -I$OPENSSL_ROOT/include/openssl" LDFLAGS="-L$OPENSSL_ROOT/lib" \
python setup.py build 

%install
python setup.py install --prefix=%i
