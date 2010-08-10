### RPM external curl 7.20.0
Source: http://curl.haxx.se/download/%n-%realversion.tar.gz
Requires: openldap
Provides: libcurl.so.3()(64bit) 

%prep
%setup -n %n-%{realversion}

%build
./configure --prefix=%i --without-libidn --disable-crypto-auth --without-ssl
make %makeprocesses

%install
make install
cd %i/lib
ln -s libcurl.so libcurl.so.3

%post
%{relocateConfig}bin/curl-config
