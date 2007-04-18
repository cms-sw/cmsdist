### RPM external curl 7.15.3
Requires: gcc-wrapper
Source: http://curl.haxx.se/download/%n-%v.tar.gz

%build
## IMPORT gcc-wrapper
./configure --prefix=%i --without-libidn
make %makeprocesses
%post
%{relocateConfig}bin/curl-config
