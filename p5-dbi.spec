### RPM external p5-dbi 1.50
## INITENV +PATH PERL5LIB %i/lib/site_perl/$PERL_VERSION/%perlarch
%define perlarch %(perl -V | tr ',' '\\n' | grep arch | cut -d= -f2)
%define downloadn DBI
Requires: perl
Source:  http://cpan.mirror.solnet.ch/authors/id/T/TI/TIMB/%{downloadn}-%{v}.tar.gz
%prep
%setup -n %downloadn-%v
%build
perl Makefile.PL LIB=%i/lib/site_perl/$PERL_VERSION
make
