### RPM external neon 0.26.3-CMS19
Source: http://www.webdav.org/%n/%n-%realversion.tar.gz

Requires: expat
%define cppflags "-I$EXPAT_ROOT/include"
%define ldflags "-L$EXPAT_ROOT/lib"

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
# bla bla
