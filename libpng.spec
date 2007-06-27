### RPM external libpng 1.2.10-CMS3
Source: ftp://ftp.simplesystems.org/pub/libpng/png/src/%{n}-%{realversion}.tar.bz2

%prep
%setup -n %n-%{realversion}
 
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
