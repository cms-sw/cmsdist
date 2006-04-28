### RPM external mysql 5.0.18
## INITENV +PATH LD_LIBRARY_PATH %i/lib/mysql

#Different download locations according to the version.

%if "%(echo %v | cut -d. -f1)" == "4"
%define source http://downloads.mysql.com/archives/mysql-4.0/%n-%v.tar.gz
%else
%define source http://mysql.belnet.be/Downloads/MySQL-5.0/mysql-%v.tar.gz
%endif

Source: %source
Requires: perl-virtual
# Let's fake the fact that we have perl (DBI) so that rpm does not complain.
Provides: perl(DBI)

%prep
%setup -n %n-%v
%ifos darwin
# There's for some reason a "-traditional-cpp", which breaks with GCC 3.3
# so remove it.  (FIXME: check if this is solved in a newer version.)
perl -p -i -e 's/-traditional-cpp/-no-cpp-precomp/g' configure.in configure
%endif

%build
CFLAGS=-O3 CXX=gcc CXXFLAGS="-O3 -felide-constructors -fno-exceptions -fno-rtti" \
   ./configure --prefix=%i --with-extra-charsets=complex \
      --enable-thread-safe-client --enable-local-infile
make %makeprocesses
%post
%{relocateConfig}bin/msql2mysql
%{relocateConfig}bin/mysqlaccess
%{relocateConfig}bin/mysqlbug
%{relocateConfig}bin/mysql_config
%{relocateConfig}bin/mysqld_multi
%{relocateConfig}bin/mysqld_safe
%{relocateConfig}bin/mysql_fix_privilege_tables
%{relocateConfig}bin/mysql_install_db


