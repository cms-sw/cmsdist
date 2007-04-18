### RPM external apt 0.5.15lorg3.2
Requires: gcc-wrapper
Source:  http://apt-rpm.org/releases/%n-%v.tar.bz2
Requires: libxml2 beecrypt rpm zlib bz2lib

%build
## IMPORT gcc-wrapper
export CFLAGS="-I$BEECRYPT_ROOT/include -I$RPM_ROOT/include"
export LDFLAGS="-L$BEECRYPT_ROOT/lib -L$RPM_ROOT/lib"
export LIBS="$LDFLAGS"
export LIBDIR="$LIBS"
export LIBXML2_CFLAGS="-I$LIBXML2_ROOT/include/libxml2 -I$BEECRYPT_ROOT/include -I$RPM_ROOT/include"
export LIBXML2_LIBS="-lxml2 -L$LIBXML2_ROOT/lib -L$BEECRYPT_ROOT/lib -L$RPM_ROOT/lib"

./configure --prefix=%{i} --exec-prefix=%{i} \
                            --disable-nls \
                            --disable-dependency-tracking \
                            --without-libintl-prefix \
                            --disable-rpath
make %makeprocesses 
