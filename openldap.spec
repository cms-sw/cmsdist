### RPM external openldap 2.4.45
## INITENV +PATH LD_LIBRARY_PATH %i/lib
Source: ftp://ftp.openldap.org/pub/OpenLDAP/%{n}-release/%{n}-%{realversion}.tgz
Requires: db6

%prep
%setup -q -n %{n}-%{realversion}

%build
# Update for AArch64 support
rm -f ./build/config.{sub,guess}
%get_config_sub ./build/config.sub
%get_config_guess ./build/config.guess
chmod +x ./build/config.{sub,guess}

./configure \
  --prefix=%{i} \
  --without-cyrus-sasl \
  --with-tls=openssl \
  --disable-static \
  --disable-slapd \
  CPPFLAGS="-I${DB6_ROOT}/include" \
  LDFLAGS="-L${DB6_ROOT}/lib"
make depend
make

%install
make install

find %{i}/lib -type f | xargs chmod 0755

# Remove man pages.
rm -rf %{i}/man
