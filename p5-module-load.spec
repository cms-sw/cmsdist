### RPM external p5-module-load 0.18
## INITENV +PATH PERL5LIB %i/lib/perl5
%define downloadn Module-Load
Source: http://search.cpan.org/CPAN/authors/id/B/BI/BINGOS/%{downloadn}-%{realversion}.tar.gz
Requires: p5-extutils-makemaker

%prep
%setup -n %downloadn-%{realversion}

%build
LC_ALL=C; export LC_ALL
perl Makefile.PL INSTALL_BASE=%i
make %{makeprocesses}

%define drop_files %i/man
