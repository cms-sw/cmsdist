### RPM external p5-extutils-makemaker 6.58
## INITENV +PATH PERL5LIB %i/lib/perl5
%define downloadn ExtUtils-MakeMaker
Source: http://search.cpan.org/CPAN/authors/id/M/MS/MSCHWERN/%{downloadn}-%{realversion}.tar.gz

%prep
%setup -n %downloadn-%{realversion}

%build
LC_ALL=C; export LC_ALL
perl Makefile.PL INSTALL_BASE=%i
make

%install
make install
rm -rf %i/man
