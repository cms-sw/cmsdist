### RPM external mysql 5.0.45-CMS18
## INITENV +PATH LD_LIBRARY_PATH %i/lib/mysql

#Different download locations according to the version.

%if "%(echo %realversion | cut -d. -f1)" == "4"
%define source http://downloads.mysql.com/archives/mysql-4.0/%n-%realversion.tar.gz
%else
%define source http://mirror.provenscaling.com/mysql/community/source/5.0/mysql-%realversion.tar.gz
%endif

Source: %source
# Let's fake the fact that we have perl (DBI) so that rpm does not complain.
Provides: perl(DBI)

%prep
%setup -n %n-%realversion
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

%install
make install
perl -p -i -e "s|^#!.*perl(.*)|#!/usr/bin/env perl$1|" $(grep -r -e "^#!.*perl.*" %i | cut -d: -f1)

# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=%n version=%v>
<Lib name=mysqlclient>
<Client>
 <Environment name=MYSQL_BASE default="%i"></Environment>
 <Environment name=LIBDIR default="$MYSQL_BASE/lib/mysql"></Environment>
 <Environment name=MYSQL_BINDIR default="$MYSQL_BASE/bin"></Environment>
 <Environment name=INCLUDE default="$MYSQL_BASE/include/mysql"></Environment>
</Client>
<Runtime name=PATH value="$MYSQL_BINDIR" type=path>
</Tool>
EOF_TOOLFILE

%post
%{relocateConfig}bin/msql2mysql
%{relocateConfig}bin/mysqlaccess
%{relocateConfig}bin/mysqlbug
%{relocateConfig}bin/mysql_config
%{relocateConfig}bin/mysqld_multi
%{relocateConfig}bin/mysqld_safe
%{relocateConfig}bin/mysql_fix_privilege_tables
%{relocateConfig}bin/mysql_install_db
%{relocateConfig}etc/scram.d/%n


