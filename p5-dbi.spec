### RPM external p5-dbi 1.50
Requires: gcc-wrapper
## INITENV +PATH PERL5LIB %i/lib/site_perl/%perlversion
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
## IMPORT gcc-wrapper
perl Makefile.PL PREFIX=%i LIB=%i/lib/site_perl/%perlversion
make
perl -p -i -e 's|^#!.*perl|#!/usr/bin/env perl|' blib/script/dbiprof
perl -p -i -e 's|^#!.*perl|#!/usr/bin/env perl|' blib/script/dbiproxy
perl -p -i -e 's|^#!.*perl|#!/usr/bin/env perl|' dbiprof
perl -p -i -e 's|^#!.*perl|#!/usr/bin/env perl|' dbiproxy
#
