### RPM external p5-dbi 1.609
## INITENV +PATH PERL5LIB %i/lib/perl5
# Dummy comment: forcing the compiling for SLC6
%define downloadn DBI
## Let's fake the provides of windows stuff for the time being.
Provides: perl(RPC::PlClient)
Provides: perl(RPC::PlServer)
Provides: perl(Win32::ODBC)
Provides: libc.so.6(GLIBC_2.3)(64bit)

Source:  http://cpan.mirror.solnet.ch/authors/id/T/TI/TIMB/%{downloadn}-%{realversion}.tar.gz
Requires: p5-extutils-makemaker

%prep
%setup -n %downloadn-%{realversion}

%build
perl Makefile.PL INSTALL_BASE=%i
make %{makeprocesses}
P=$(which perl)
perl -p -i -e 's|^#!.*perl|#!'"$P"'|' blib/script/dbiprof
perl -p -i -e 's|^#!.*perl|#!'"$P"'|' blib/script/dbiproxy
perl -p -i -e 's|^#!.*perl|#!'"$P"'|' dbiprof
perl -p -i -e 's|^#!.*perl|#!'"$P"'|' dbiproxy

%define drop_files %i/man
