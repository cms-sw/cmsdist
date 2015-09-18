### RPM external openldap 2.4.33
## INITENV +PATH LD_LIBRARY_PATH %i/lib
Source: ftp://ftp.openldap.org/pub/OpenLDAP/openldap-release/%n-%realversion.tgz
Requires: openssl db4 

%prep
%setup -q -n %n-%{realversion}

%build
export CPPFLAGS="-I${OPENSSL_ROOT}/include"
export LDFLAGS="-L${OPENSSL_ROOT}/lib"
./configure --prefix=%i --without-cyrus-sasl --with-tls=openssl --disable-static --disable-slapd --disable-slurpd
make depend
make %{makeprocesses}

%install
make install
# Read documentation online.
rm -rf %i/man
