### RPM external openldap 2.4.45
## INITENV +PATH LD_LIBRARY_PATH %i/lib
Source: ftp://ftp.openldap.org/pub/OpenLDAP/%{n}-release/%{n}-%{realversion}.tgz
Requires: openssl db6

%prep
%setup -q -n %{n}-%{realversion}

%build
# Update for AArch64 support
rm -f ./build/config.{sub,guess}
curl -L -k -s -o ./build/config.sub 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.sub;hb=HEAD'
curl -L -k -s -o ./build/config.guess 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.guess;hb=HEAD'
chmod +x ./build/config.{sub,guess}

./configure \
  --prefix=%{i} \
  --without-cyrus-sasl \
  --with-tls=openssl \
  --disable-static \
  --disable-slapd \
  CPPFLAGS="-I${OPENSSL_ROOT}/include -I${DB6_ROOT}/include" \
  LDFLAGS="-L${OPENSSL_ROOT}/lib -L${DB6_ROOT}/lib"
make depend
make

%install
make install

find %{i}/lib -type f | xargs chmod 0755

# Remove man pages.
rm -rf %{i}/man
# bla bla
