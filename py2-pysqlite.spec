### RPM external py2-pysqlite 2.8.3
## INITENV +PATH PYTHON27PATH %{i}/${PYTHON_LIB_SITE_PACKAGES}


%define pip_name pysqlite
Requires: sqlite py2-setuptools 
%define PipPreBuild tar xfz pysqlite-%{realversion}.tar.gz;rm pysqlite-%{realversion}.tar.gz;echo "include_dirs=$SQLITE_ROOT/include">>pysqlite-%{realversion}/setup.cfg;tar cfz pysqlite-%{realversion}.tar.gz pysqlite-%{realversion}
#echo "include_dirs=$SQLITE_ROOT/include"\>\>pysqlite-2.8.3/setup.cfg;

## IMPORT build-with-pip

