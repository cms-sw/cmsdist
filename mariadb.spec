### RPM external mariadb 10.0.12
## INITENV +PATH %{dynamic_path_var} %i/lib/mysql
## INITENV +PATH PATH %i/scripts
## INITENV SET MYSQL_HOME $MYSQL_ROOT
%define source http://mirrors.syringanetworks.net/mariadb/mariadb-%realversion/source/mariadb-%realversion.tar.gz
Source: %source
Requires: zlib openssl ncurses libxml2
BuildRequires: cmake

%prep
%setup -n %n-%realversion

%build
cmake .  -DCURSES_LIBRARY=${NCURSES_ROOT}/lib/libncurses.a \
         -DCURSES_INCLUDE_PATH=${NCURSES_ROOT}/include \
         -DZLIB_LIBRARY=${ZLIB_ROOT}/lib/libz.so \
         -DZLIB_INCLUDE_DIR=${ZLIB_ROOT}/include \
         -DOPENSSL_LIBRARIES=${OPENSSL_ROOT}/lib/libssl.so \
         -DOPENSSL_INCLUDE_DIR=${OPENSSL_ROOT}/include \
         -DCRYPTO_LIBRARY=${OPENSSL_ROOT}/lib/libcrypto.so \
         -DLIBXML2_LIBRARIES=${LIBXML2_ROOT}/lib/libxml2.so \
         -DLIBXML2_INCLUDE_DIR=${LIBXML2_ROOT}/include/libxml2 \
         -DHAVE_VIDATTR:INTERNAL=0 \
         -DHAVE_SETUPTERM:INTERNAL=0 \
         -DCMAKE_INSTALL_PREFIX=%i \
         -DWITH_EXTRA_CHARSETS=complex \
         -DENABLED_LOCAL_INFILE=1

make
%install
make install

# Need to add this sed command and set basedir directory at mysql_isntall_db file.
# Because of this problem when starting MySQL: "FATAL ERROR: Could not find ./bin/my_print_defaults"
sed -iback 's|^basedir=""|basedir="%{i}"|' %i/scripts/mysql_install_db
rm -f %i/scripts/mysql_install_dbback

rm -fR %i/mysql-test

# Strip libraries, we are not going to debug them.
%define strip_files %i/lib

# Look up documentation online; don't need archive libraries.
%define drop_files %i/share/{man,info} %i/lib/mysql/plugin/*.{l,}a %i/lib/mysql/libmysqlclient*.{l,}a

%post
%{relocateConfig}bin/msql2mysql
%{relocateConfig}bin/mysqlaccess
%{relocateConfig}bin/mysql_config
%{relocateConfig}bin/mysqld_multi
%{relocateConfig}bin/mysqld_safe
%{relocateConfig}bin/mysql_secure_installation
%{relocateConfig}bin/my_print_defaults
%{relocateConfig}docs/INFO_BIN
%{relocateConfig}include/mysql/my_config.h
%{relocateConfig}include/mysql/private/config.h
%{relocateConfig}scripts/mysql_install_db
%{relocateConfig}support-files/my-huge.cnf
%{relocateConfig}support-files/my-large.cnf
%{relocateConfig}support-files/my-medium.cnf
%{relocateConfig}support-files/my-small.cnf
%{relocateConfig}support-files/mysql-log-ro
