### RPM external p5-params-check 0.28
## INITENV +PATH PERL5LIB %i/lib/perl5
%define downloadn Params-Check
Source: http://search.cpan.org/CPAN/authors/id/B/BI/BINGOS/%{downloadn}-%{realversion}.tar.gz
Requires: p5-extutils-makemaker p5-locale-maketext-simple

%prep
%setup -n %downloadn-%{realversion}

%build
LC_ALL=C; export LC_ALL
perl Makefile.PL INSTALL_BASE=%i
make %{makeprocesses}

%define drop_files %i/man
