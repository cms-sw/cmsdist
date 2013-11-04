### RPM external mysql 5.1.58
## INITENV +PATH %{dynamic_path_var} %i/lib/mysql
## INITENV SET MYSQL_HOME $MYSQL_ROOT

#Different download locations according to the version.

%if "%(echo %realversion | cut -d. -f1)" == "4"
%define source http://downloads.mysql.com/archives/mysql-4.0/%n-%realversion.tar.gz
%else
#%define source http://mirror.provenscaling.com/mysql/community/source/5.0/mysql-%realversion.tar.gz
#%define source http://opensource.become.com/mysql/Downloads/MySQL-5.1/mysql-%realversion.tar.gz
%define source http://downloads.mysql.com/archives/mysql-5.1/mysql-%realversion.tar.gz
%endif

Source: %source
# Let's fake the fact that we have perl (DBI) so that rpm does not complain.
Provides: perl(DBI)
Requires: zlib
BuildRequires: autotools

%prep
%setup -n %n-%realversion
%if "%(case %cmsplatf in (osx*_*_gcc421) echo true ;; (*) echo false ;; esac)" == "true"
# There's for some reason a "-traditional-cpp", which breaks with GCC 3.3
# so remove it.  (FIXME: check if this is solved in a newer version.)
perl -p -i -e 's/-traditional-cpp/-no-cpp-precomp/g' configure.in configure
autoreconf -i -f
%endif

%build
CFLAGS=-O3 CXX=gcc CXXFLAGS="-O3 -felide-constructors -fno-exceptions -fno-rtti" \
   ./configure --prefix=%i --with-extra-charsets=complex \
      --enable-thread-safe-client --enable-local-infile \
      --disable-static --with-zlib-dir=$ZLIB_ROOT \
      --without-docs --without-man \
      --with-plugins=innobase
make %makeprocesses

%install
make install
perl -p -i -e "s|^#!.*perl(.*)|#!/usr/bin/env perl$1|" $(grep -r -e "^#!.*perl.*" %i | cut -d: -f1)
rm -fR %i/mysql-test

mkdir -p %i/etc
cat << \EOF > %i/etc/my.cnf
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

innodb_thread_concurrency=0
innodb_concurrency_tickets=10000
innodb_commit_concurrency=0
innodb_flush_logs_at_trx_commit=0
innodb_flush_method=O_DIRECT
innodb_file_io_threads = 4
innodb_checksums=0
innodb_doublewrite=0
innodb_data_file_path = ibdata1:2047M;ibdata2:2000M:autoextend

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

# Strip libraries, we are not going to debug them.
%define strip_files %i/lib

# Look up documentation online; don't need archive libraries.
%define drop_files %i/share/{man,info} %i/lib/mysql/plugin/*.{l,}a %i/lib/mysql/libmysqlclient*.{l,}a

%post
%{relocateConfig}bin/msql2mysql
%{relocateConfig}bin/mysqlaccess
%{relocateConfig}bin/mysqlbug
%{relocateConfig}bin/mysql_config
%{relocateConfig}bin/mysqld_multi
%{relocateConfig}bin/mysqld_safe
%{relocateConfig}bin/mysql_fix_privilege_tables
%{relocateConfig}bin/mysql_install_db

