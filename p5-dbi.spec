### RPM external p5-dbi 1.609
## INITENV +PATH PERL5LIB %i/lib/site_perl/%perlversion

%define perl /usr/bin/env perl
%if "%(echo %cmsplatf | cut -f1 -d_ | sed -e 's|\([A-Za-z]*\)[0-9]*|\1|')" == "osx"
%define perl /usr/bin/perl
%endif

%define perlversion %(%perl -e 'printf "%%vd", $^V')
%define perlarch %(%perl -MConfig -e 'print $Config{archname}')
%define downloadn DBI
## Let's fake the provides of windows stuff for the time being.
Provides: perl(RPC::PlClient)
Provides: perl(RPC::PlServer)
Provides: perl(Win32::ODBC)
Provides: libc.so.6(GLIBC_2.3)(64bit)

Source:  http://cpan.mirror.solnet.ch/authors/id/T/TI/TIMB/%{downloadn}-%{realversion}.tar.gz
%prep
%setup -n %downloadn-%{realversion}
%build
%perl Makefile.PL PREFIX=%i LIB=%i/lib/site_perl/%perlversion
make
%perl -p -i -e 's|^#!.*perl|#!%perl|' blib/script/dbiprof
%perl -p -i -e 's|^#!.*perl|#!%perl|' blib/script/dbiproxy
%perl -p -i -e 's|^#!.*perl|#!%perl|' dbiprof
%perl -p -i -e 's|^#!.*perl|#!%perl|' dbiproxy
make install

%install
