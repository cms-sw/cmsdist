### RPM external mysql 5.1.35
## INITENV +PATH LD_LIBRARY_PATH %i/lib/mysql
## INITENV SET MYSQL_HOME $MYSQL_ROOT

#Different download locations according to the version.

%if "%(echo %realversion | cut -d. -f1)" == "4"
%define source http://downloads.mysql.com/archives/mysql-4.0/%n-%realversion.tar.gz
%else
#%define source http://mirror.provenscaling.com/mysql/community/source/5.0/mysql-%realversion.tar.gz
%define source http://opensource.become.com/mysql/Downloads/MySQL-5.1/mysql-%realversion.tar.gz
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
rm -fR %i/mysql-test

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

# setup approripate links and made post install procedure
. $RPM_INSTALL_PREFIX/%{pkgrel}/etc/profile.d/init.sh
cat > $MYSQL_ROOT/etc/my.cnf << EOF
[mysqld]
max_allowed_packet=128M

max_connections = 1000
connect_timeout = 60

set-variable = innodb_log_file_size=512M
set-variable = innodb_log_buffer_size=8M
set-variable = innodb_buffer_pool_size=2G
set-variable = innodb_additional_mem_pool_size=50M

key_buffer=512M

query_cache_type=1
query_cache_limit=10M
query_cache_size=128M

# inodb
innodb_thread_concurrency=0
innodb_concurrency_tickets=10000
innodb_commit_concurrency=0
innodb_flush_logs_at_trx_commit=0
innodb_flush_method=O_DIRECT
innodb_file_io_threads = 4
innodb_checksums=0
innodb_doublewrite=0


max_heap_table_size=1024M
tmp_table_size=1024M

long_query_time=5
innodb_sync_spin_loops=60

innodb_force_recovery = 0
innodb_lock_wait_timeout = 100
innodb_autoinc_lock_mode = 2


[mysql.server]
STRICT_TRANS_TABLES=1
transaction-isolation = READ-COMMITTED
EOF

