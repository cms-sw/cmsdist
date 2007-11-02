### RPM external neon 0.26.3-CMS18

Source: http://www.webdav.org/%n/%n-%realversion.tar.gz
Requires: expat
%if "%{?online_release:set}" != "set"
Requires: openssl zlib
%endif

%prep
%setup -n %n-%realversion

%build

export CFLAGS="-fPIC -g -O2" 

%if "%{?online_release:set}" != "set"
export CPPFLAGS="-I$EXPAT_ROOT/include -I$ZLIB_ROOT/include -I$OPENSSL_ROOT/include"
export LDFLAGS="-L$EXPAT_ROOT/lib -L$ZLIB_ROOT/lib -L$OPENSSL_ROOT/lib"
%else
export CPPFLAGS="-I$EXPAT_ROOT/include"
export LDFLAGS="-L$EXPAT_ROOT/lib"
%endif

./configure --enable-shared --prefix=%i --with-pic --without-zlib  --without-gssapi --with-expat 
make -j %makeprocesses
%post
%{relocateConfig}lib/libneon.la
