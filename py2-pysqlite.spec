### RPM external py2-pysqlite 2.8.3
## IMPORT build-with-pip

%define doPython3 no
Requires: sqlite py2-setuptools 
%define PipPreBuild tar xfz pysqlite-%{realversion}.tar.gz;rm pysqlite-%{realversion}.tar.gz;echo "include_dirs=$SQLITE_ROOT/include">>pysqlite-%{realversion}/setup.cfg;tar cfz pysqlite-%{realversion}.tar.gz pysqlite-%{realversion}
