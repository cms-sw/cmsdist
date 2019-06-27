### RPM external p5-compress-zlib 1.42
## INITENV +PATH PERL5LIB %i/lib/perl5
%define downloadn Compress-Zlib
Source: http://search.cpan.org/CPAN/authors/id/P/PM/PMQS/%{downloadn}-%{realversion}.tar.gz
Requires: zlib p5-extutils-makemaker

%prep
%setup -n %downloadn-%realversion

%build
LC_ALL=C; export LC_ALL
perl Makefile.PL INSTALL_BASE=%i INCLUDE=$ZLIB_ROOT/include
make

%define drop_files %i/man

%post
%{relocateConfig}lib/perl5/x86_64-linux-thread-multi/perllocal.pod
%{relocateConfig}lib/perl5/x86_64-linux-thread-multi/auto/Compress/Zlib/.packlist
# bla bla
