### RPM external p5-dbi 1.50
## INITENV +PATH PERL5LIB %i/lib/site_perl/%perlversion/%perlarch
%define perlversion %(perl -e 'printf "%%vd", $^V')
%define perlarch %(perl -MConfig -e 'print $Config{archname}')
%define downloadn DBI
## Let's fake the provides of windows stuff for the time being.
Provides: perl(RPC::PlClient)
Provides: perl(RPC::PlServer)
Provides: perl(Win32::ODBC)

Source:  http://cpan.mirror.solnet.ch/authors/id/T/TI/TIMB/%{downloadn}-%{v}.tar.gz
%prep
%setup -n %downloadn-%v
%build
perl Makefile.PL PREFIX=%i LIB=%i/lib/site_perl/%perlversion
make
