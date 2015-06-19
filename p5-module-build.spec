### RPM external p5-module-build 0.3800
## INITENV +PATH PERL5LIB %i/lib/perl5
%define downloadn Module-Build
Source: http://search.cpan.org/CPAN/authors/id/D/DA/DAGOLDEN/%{downloadn}-%{realversion}.tar.gz
Requires: p5-extutils-makemaker
Requires: p5-cpan-meta p5-parse-cpan-meta
Requires: p5-extutils-cbuilder p5-extutils-parsexs
Requires: p5-perl-ostype p5-version p5-module-metadata p5-test-harness

%prep
%setup -n %downloadn-%{realversion}

%build
LC_ALL=C; export LC_ALL
perl Makefile.PL INSTALL_BASE=%i
make %{makeprocesses}

%define drop_files %i/man
