### RPM external p5-dbi 1.50
## INITENV +PATH PERL5LIB %i/lib/site_perl/$PERL_VERSION/%perlarch
%define perlarch $(perl -e 'use Config; print $Config{archname}')
%define downloadn DBI
## Let's fake the provides of windows stuff for the time being.
Provides: perl(RPC::PlClient)
Provides: perl(RPC::PlServer)
Provides: perl(Win32::ODBC)

Requires: perl-virtual
Source:  http://cpan.mirror.solnet.ch/authors/id/T/TI/TIMB/%{downloadn}-%{v}.tar.gz
%prep
%setup -n %downloadn-%v
%build
perl Makefile.PL LIB=%i/lib/site_perl/$PERL_VERSION PREFIX=%i
make
