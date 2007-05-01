### RPM external libpng 1.2.10
 
Source: ftp://ftp.simplesystems.org/pub/libpng/png/src/%{n}-%{v}.tar.bz2

%build
./configure --prefix=%{i}
make %makeprocesses
%post
%{relocateConfig}bin/libpng-config
%{relocateConfig}bin/libpng12-config
%{relocateConfig}lib/libpng.la
%{relocateConfig}lib/libpng12.la
%{relocateConfig}lib/pkgconfig/libpng.pc
%{relocateConfig}lib/pkgconfig/libpng12.pc
