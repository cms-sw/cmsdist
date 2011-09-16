### RPM external libxslt 1.1.26

# 64-bit version
Provides: libgcrypt.so.11()(64bit)
Provides: libgcrypt.so.11(GCRYPT_1.2)(64bit)
Provides: libgpg-error.so.0()(64bit)

Source: ftp://xmlsoft.org/%n/%n-%realversion.tar.gz

Requires: libxml2

%prep
%setup -n libxslt-%realversion
%build
./configure --prefix=%i --with-libxml-prefix=$LIBXML2_ROOT
make %makeprocesses

%install
make install

# Remove pkg-config to avoid rpm-generated dependency on /usr/bin/pkg-config
# which we neither need nor use at this time.
rm -rf %i/lib/pkgconfig

# Strip libraries, we are not going to debug them.
find %i/lib -type f -perm -a+x -exec strip {} \;

# Don't need archive libraries.
rm -f %i/lib/*.{l,}a

# Look up documentation online.
rm -rf %i/share/{doc,man}

%post
%{relocateConfig}bin/xslt-config
