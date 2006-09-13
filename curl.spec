### RPM external curl 7.10.8
Source: http://curl.haxx.se/download/archeology/%n-%v.tar.gz

%build
./configure --prefix=%i
make %makeprocesses
%post
%{relocateConfig}bin/curl-config
