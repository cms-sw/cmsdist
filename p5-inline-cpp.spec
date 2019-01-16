### RPM external p5-inline-cpp 0.39
## INITENV +PATH PERL5LIB %i/lib/perl5
%define downloadn Inline-CPP
Source: https://cpan.metacpan.org/authors/id/D/DA/DAVIDO/%{downloadn}-%{realversion}.tar.gz
Requires: gcc p5-extutils-makemaker p5-inline-c p5-file-sharedir p5-file-sharedir-install p5-inline p5-pegex p5-parse-recdescent

%prep
%setup -n %downloadn-%realversion

%build
LC_ALL=C; export LC_ALL
export PERL_MM_USE_DEFAULT=1
perl Makefile.PL INSTALL_BASE=%i
make %{makeprocesses}

%define drop_files %i/man
