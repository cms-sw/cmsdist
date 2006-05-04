### RPM external p5-time-hires 1.66
## INITENV +PATH PERL5LIB %i/lib/site_perl/$PERL_VERSION/%perlarch
%define perlarch %(perl -e 'use Config; print $Config{archname}')
%define downloadn Time-HiRes

Requires: perl-virtual
Source: http://search.cpan.org/CPAN/authors/id/J/JH/JHI/%{downloadn}-%{v}.tar.gz
%prep
%setup -n %downloadn-%v
%build
LC_ALL=C; export LC_ALL
perl Makefile.PL LIB=%i/lib/site_perl/$PERL_VERSION PREFIX=%i
make
