### RPM external unixodbc 2.2.11
%define downloadn unixODBC
Source: http://www.unixodbc.org/%downloadn-%v.tar.gz
%prep
%setup -n %{downloadn}-%{v}
%build
./configure --prefix=%{i} --disable-gui
make %makeprocesses
mkdir -p %i/etc
echo "
  [MyODBC]
   Description  = MySQL ODBC 3.51 driver for Linux
   Driver  = libmyodbc3.so
   FileUsage  = 1
      
  [MySQL]
   Description  = MySQL ODBC 3.51 driver for Linux
   Driver  = libmyodbc3.so
   FileUsage  = 1
          
  [ODBC]
   Trace      = Yes
   TraceFile  = /tmp/pool_sql.log
   ForceTrace = Yes
   Pooling    = No
" > %i/etc/odbcinst.ini
