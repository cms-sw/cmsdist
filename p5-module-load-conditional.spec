### RPM external p5-module-load-conditional 0.44
## INITENV +PATH PERL5LIB %i/lib/perl5
%define downloadn Module-Load-Conditional
Source: http://search.cpan.org/CPAN/authors/id/B/BI/BINGOS/%{downloadn}-%{realversion}.tar.gz
Requires: p5-extutils-makemaker p5-locale-maketext-simple p5-module-load p5-params-check

%prep
%setup -n %downloadn-%{realversion}

%build
LC_ALL=C; export LC_ALL
perl Makefile.PL INSTALL_BASE=%i
make %{makeprocesses}

%define drop_files %i/man
