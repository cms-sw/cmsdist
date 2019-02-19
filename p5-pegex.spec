### RPM external p5-pegex 0.70
## INITENV +PATH PERL5LIB %i/lib/perl5
%define downloadn Pegex
Source: https://cpan.metacpan.org/authors/id/I/IN/INGY/%{downloadn}-%{realversion}.tar.gz
Requires: p5-extutils-makemaker p5-file-sharedir-install

%prep
%setup -n %downloadn-%realversion

%build
LC_ALL=C; export LC_ALL
perl Makefile.PL INSTALL_BASE=%i
make %{makeprocesses}

%define drop_files %i/man
