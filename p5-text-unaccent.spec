### RPM external p5-text-unaccent 1.08
## INITENV +PATH PERL5LIB %i/lib/perl5
%define downloadn Text-Unaccent
Source: http://cpan.perl.org/modules/by-module/Text/%{downloadn}-%{realversion}.tar.gz
Requires: p5-extutils-makemaker

%prep
%setup -n %downloadn-%realversion

%build
LC_ALL=C; export LC_ALL
perl Makefile.PL INSTALL_BASE=%i
make %{makeprocesses}

%define drop_files %i/man
