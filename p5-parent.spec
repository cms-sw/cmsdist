### RPM external p5-parent 0.237
## INITENV +PATH PERL5LIB %i/lib/perl5
%define downloadn parent
Source: https://cpan.metacpan.org/authors/id/C/CO/CORION/%{downloadn}-%{realversion}.tar.gz
Requires: p5-extutils-makemaker

%prep
%setup -n %downloadn-%realversion

%build
LC_ALL=C; export LC_ALL
perl Makefile.PL INSTALL_BASE=%i
make %{makeprocesses}

%define drop_files %i/man
