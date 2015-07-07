### RPM external p5-cpan-meta 2.110930
## INITENV +PATH PERL5LIB %i/lib/perl5
%define downloadn CPAN-Meta
Source: http://search.cpan.org/CPAN/authors/id/D/DA/DAGOLDEN/%{downloadn}-%{realversion}.tar.gz
Requires: p5-extutils-makemaker p5-parse-cpan-meta p5-version

%prep
%setup -n %downloadn-%{realversion}

%build
LC_ALL=C; export LC_ALL
perl Makefile.PL INSTALL_BASE=%i
make %{makeprocesses}

%define drop_files %i/man
