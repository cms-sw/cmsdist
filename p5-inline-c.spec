### RPM external p5-inline-c 0.78
## INITENV +PATH PERL5LIB %i/lib/perl5
%define downloadn Inline-C
Source: https://cpan.metacpan.org/authors/id/T/TI/TINITA/%{downloadn}-%{realversion}.tar.gz
Requires: p5-extutils-makemaker p5-file-sharedir p5-file-sharedir-install p5-inline p5-pegex p5-parse-recdescent

%prep
%setup -n %downloadn-%realversion

%build
LC_ALL=C; export LC_ALL
perl Makefile.PL INSTALL_BASE=%i
make %{makeprocesses}

%define drop_files %i/man
