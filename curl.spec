### RPM external curl 7.15.3-CMS3
Source: http://curl.haxx.se/download/%n-%realversion.tar.gz

%prep
%setup -n %n-%{realversion}

%build
./configure --prefix=%i --without-libidn
make %makeprocesses
%post
%{relocateConfig}bin/curl-config
