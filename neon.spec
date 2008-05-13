### RPM external neon 0.26.3-CMS19
Source: http://www.webdav.org/%n/%n-%realversion.tar.gz

Requires: expat
%if "%cmsplatf" != "slc4onl_ia32_gcc346"
Requires: openssl zlib
%endif

%define cppflags "-I$EXPAT_ROOT/include -I$ZLIB_ROOT/include -I$OPENSSL_ROOT/include"
%define ldflags "-L$EXPAT_ROOT/lib -L$ZLIB_ROOT/lib -L$OPENSSL_ROOT/lib"

%if "%(echo %{cmsos} | sed -e 's|slc.online_.*|online|')" == "online"
%define cppflags "-I$EXPAT_ROOT/include"
%define ldflags "-L$EXPAT_ROOT/lib"
%endif


%prep
%setup -n %n-%realversion

%build

export CFLAGS="-fPIC -g -O2" 

export CPPFLAGS=%{cppflags}
export LDFLAGS=%{ldflags}

./configure --enable-shared --prefix=%i --with-pic --without-zlib  --without-gssapi --with-expat 
make -j %makeprocesses
%post
%{relocateConfig}lib/libneon.la
