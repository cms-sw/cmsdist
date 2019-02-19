### RPM external p5-uri 1.74
## INITENV +PATH PERL5LIB %i/lib/perl5
%define downloadn URI
Source: https://cpan.metacpan.org/authors/id/E/ET/ETHER/%{downloadn}-%{realversion}.tar.gz
Requires: p5-extutils-makemaker p5-parent

%prep
%setup -n %downloadn-%realversion

%build
LC_ALL=C; export LC_ALL
perl Makefile.PL INSTALL_BASE=%i
make %{makeprocesses}

%define drop_files %i/man
