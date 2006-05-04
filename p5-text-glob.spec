### RPM external p5-text-glob 0.06
## INITENV +PATH PERL5LIB %i/lib/site_perl/$PERL_VERSION/%perlarch
%define perlarch %(perl -e 'use Config; print $Config{archname}')
%define downloadn Text-Glob

Requires: perl-virtual
Source: http://search.cpan.org/CPAN/authors/id/R/RC/RCLAMP/%{downloadn}-%{v}.tar.gz
%prep
%setup -n %downloadn-%v
%build
LC_ALL=C; export LC_ALL
perl Makefile.PL LIB=%i/lib/site_perl/$PERL_VERSION PREFIX=%i
make
