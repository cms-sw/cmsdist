### RPM external curl 7.20.0
Source: http://curl.haxx.se/download/%n-%realversion.tar.gz
Provides: libcurl.so.3()(64bit) 

%prep
%setup -n %n-%{realversion}

%build
./configure --prefix=%i --without-libidn --disable-crypto-auth --disable-ldap --without-ssl
# This should change link from "-lz" to "-lrt -lz", needed by gold linker
# This is a fairly ugly way to do it, however.
perl -p -i -e "s!\(LIBS\)!(LIBCURL_LIBS)!" src/Makefile
make %makeprocesses

%install
make install
cd %i/lib
ln -s libcurl.so libcurl.so.3

%post
%{relocateConfig}bin/curl-config
