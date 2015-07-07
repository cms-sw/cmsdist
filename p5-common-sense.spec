### RPM external p5-common-sense 3.4
## INITENV +PATH PERL5LIB %i/lib/perl5
%define downloadn common-sense
Source: http://search.cpan.org/CPAN/authors/id/M/ML/MLEHMANN/%{downloadn}-%{realversion}.tar.gz
Requires: p5-extutils-makemaker

%prep
%setup -n %downloadn-%realversion

%build
LC_ALL=C; export LC_ALL
perl Makefile.PL INSTALL_BASE=%i
make %{makeprocesses}

%define drop_files %i/man
