### RPM external p5-dbi 1.50-CMS19
## INITENV +PATH PERL5LIB %i/lib/site_perl/%perlversion
%define perlversion %(perl -e 'printf "%%vd", $^V')
%define perlarch %(perl -MConfig -e 'print $Config{archname}')
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
perl Makefile.PL PREFIX=%i LIB=%i/lib/site_perl/%perlversion
make
perl -p -i -e 's|^#!.*perl|#!/usr/bin/env perl|' blib/script/dbiprof
perl -p -i -e 's|^#!.*perl|#!/usr/bin/env perl|' blib/script/dbiproxy
perl -p -i -e 's|^#!.*perl|#!/usr/bin/env perl|' dbiprof
perl -p -i -e 's|^#!.*perl|#!/usr/bin/env perl|' dbiproxy

case %{cmsos} in
    slc4_ia32)
    if ldd /usr/bin/gcc | grep -q /lib64/
    then
        make install
        mv %i/lib/site_perl/%perlversion/x86_64-linux-thread-multi  %i/lib/site_perl/%perlversion/i386-linux-thread-multi
        make clean
        export PATH=/usr/bin/:$PATH
        export GCC_EXEC_PREFIX=/usr/lib/gcc/
        perl Makefile.PL PREFIX=%i LIB=%i/lib/site_perl/%perlversion
        make
        perl -p -i -e 's|^#!.*perl|#!/usr/bin/env perl|' blib/script/dbiprof
        perl -p -i -e 's|^#!.*perl|#!/usr/bin/env perl|' blib/script/dbiproxy
        perl -p -i -e 's|^#!.*perl|#!/usr/bin/env perl|' dbiprof
        perl -p -i -e 's|^#!.*perl|#!/usr/bin/env perl|' dbiproxy
    fi;;
    *)
    ;;
esac
#
# bla bla
