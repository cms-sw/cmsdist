### RPM external p5-io-zlib 1.10
## INITENV +PATH PERL5LIB %i/lib/perl5
%define downloadn IO-Zlib
Source: http://search.cpan.org/CPAN/authors/id/T/TO/TOMHUGHES/%{downloadn}-%{realversion}.tar.gz
Requires: p5-extutils-makemaker

%prep
%setup -n %downloadn-%realversion

%build
LC_ALL=C; export LC_ALL
perl Makefile.PL INSTALL_BASE=%i
make %{makeprocesses}

%define drop_files %i/man
