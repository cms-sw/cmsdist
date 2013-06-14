### RPM external apr-util 1.2.6
Source: http://mirror.switch.ch/mirror/apache/dist/apr/%{n}-%{v}.tar.gz
Requires: apr mysql sqlite expat 
%build
./configure --prefix=%{i} \
            --with-apr=$APR_ROOT \
            --with-mysql=$MYSQL_ROOT \
            --with-sqlite3=$SQLITE_ROOT \
            --with-expat=$EXPAT_ROOT
make %makeprocesses
