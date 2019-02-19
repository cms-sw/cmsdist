### RPM external p5-file-sharedir 1.116
## INITENV +PATH PERL5LIB %i/lib/perl5
%define downloadn File-ShareDir
Source: https://cpan.metacpan.org/authors/id/R/RE/REHSACK/%{downloadn}-%{realversion}.tar.gz
Requires: p5-extutils-makemaker p5-class-inspector

%prep
%setup -n %downloadn-%realversion

%build
LC_ALL=C; export LC_ALL
perl Makefile.PL INSTALL_BASE=%i
make %{makeprocesses}

%define drop_files %i/man
