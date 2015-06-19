### RPM external p5-test-simple 0.98
## INITENV +PATH PERL5LIB %i/lib/perl5
%define downloadn Test-Simple
Source: http://search.cpan.org/CPAN/authors/id/M/MS/MSCHWERN/%{downloadn}-%{realversion}.tar.gz
Requires: p5-extutils-makemaker

%prep
%setup -n %downloadn-%{realversion}

%build
LC_ALL=C; export LC_ALL
perl Makefile.PL INSTALL_BASE=%i
make %{makeprocesses}

%define drop_files %i/man
