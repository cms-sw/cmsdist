### RPM external libpng 1.2.10
Source: http://riksun.riken.go.jp/pub/pub/Linux/slackware/slackware-current/source/l/libpng/%{n}-%{realversion}.tar.bz2
Requires: zlib
%prep
%setup -n %n-%{realversion}
 
%build
./configure --prefix=%{i}
make %makeprocesses

%install
make install

%post
%{relocateConfig}bin/libpng-config
%{relocateConfig}bin/libpng12-config
%{relocateConfig}lib/libpng.la
%{relocateConfig}lib/libpng12.la
%{relocateConfig}lib/pkgconfig/libpng.pc
%{relocateConfig}lib/pkgconfig/libpng12.pc
