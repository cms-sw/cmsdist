### RPM external cyrus-sasl 2.1.25
Source: http://ftp.andrew.cmu.edu/pub/cyrus-mail/cyrus-sasl-2.1.25.tar.gz

Requires: openssl nss

%prep
%setup -q -n %{n}-%{realversion}

%build
LDFLAGS="-L${OPENSSL_ROOT}/lib"
./configure --prefix=%{i} --with-openssl=${OPENSSL_ROOT} LDFLAGS="${LDFLAGS}"
make

%install
make install

# Remove archives
find ./lib \( -name '*.a' -o -name '*.la' \) -exec rm -f {} \;
