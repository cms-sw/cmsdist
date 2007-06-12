### RPM external neon 0.26.3

Source: http://www.webdav.org/%n/%n-%realversion.tar.gz
Requires: openssl expat zlib

%build
export CPPFLAGS="-I$EXPAT_ROOT/include -I$ZLIB_ROOT/include -I$OPESSL_ROOT/include -I$EXPAT_ROOT/include"
export CFLAGS="-fPIC -g -O2" 
export LDFLAGS="-L$EXPAT_ROOT/lib -L$ZLIB_ROOT/lib -L$OPENSSL_ROOT/lib"
./configure --enable-shared --prefix=%i --with-pic --without-zlib --with-expat 
make -j %makeprocesses
%post
%{relocateConfig}lib/libneon.la
