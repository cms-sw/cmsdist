### RPM external curl 7.15.3
Source: http://curl.haxx.se/download/%n-%v.tar.gz

%build
./configure --prefix=%i
make %makeprocesses
%post
%{relocateConfig}bin/curl-config
