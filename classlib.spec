### RPM external classlib 3.1.0
Source: http://cmsmac01.cern.ch/~lat/exports/%n-%realversion.tar.bz2
Requires: zlib bz2lib pcre openssl lzo xz

%prep
%setup -n %n-%realversion

%build
./configure --prefix=%i                         \
  --with-zlib-includes=$ZLIB_ROOT/include       \
  --with-zlib-libraries=$ZLIB_ROOT/lib          \
  --with-bz2lib-includes=$BZ2LIB_ROOT/include   \
  --with-bz2lib-libraries=$BZ2LIB_ROOT/lib      \
  --with-pcre-includes=$PCRE_ROOT/include       \
  --with-pcre-libraries=$PCRE_ROOT/lib          \
  --with-openssl-includes=$OPENSSL_ROOT/include \
  --with-openssl-libraries=$OPENSSL_ROOT/lib    \
  --with-lzo-includes=$LZO_ROOT/include         \
  --with-lzo-libraries=$LZO_ROOT/lib            \
  --with-lzma-includes=$XZ_ROOT/include         \
  --with-lzma-libraries=$XZ_ROOT/lib

make %makeprocesses

%install
make %makeprocesses install
