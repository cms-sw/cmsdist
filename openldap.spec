### RPM external openldap 2.4.33
## INITENV +PATH LD_LIBRARY_PATH %i/lib
Source: ftp://ftp.openldap.org/pub/OpenLDAP/openldap-release/%n-%realversion.tgz
Requires: openssl db4 

%prep
%setup -q -n %n-%{realversion}

%build
./configure --prefix=%i --without-cyrus-sasl --with-tls --disable-static --disable-slapd --disable-slurpd
make depend
make %{makeprocesses}

%install
make install
# Read documentation online.
rm -rf %i/man
