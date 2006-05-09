### RPM external oracle 10.2.0.1
## INITENV SET ORACLE_HOME %i
## INITENV +PATH SQLPATH %i/bin
Source0: http://oraclelon1.oracle.com/otn/linux/instantclient/10201/instantclient-basic-linux32-10.2.0.1-20050713.zip
Source1: http://oraclelon1.oracle.com/otn/linux/instantclient/10201/instantclient-sdk-linux32-10.2.0.1-20050713.zip
Source2: http://oraclelon1.oracle.com/otn/linux/instantclient/10201/instantclient-sqlplus-linux32-10.2.0.1-20050713.zip

%prep
unzip -f %_sourcedir/instantclient-basic*.zip
unzip -f %_sourcedir/instantclient-sdk*.zip
unzip -f %_sourcedir/instantclient-sqlplus*.zip
%build
%install
mkdir -p %i/bin %i/etc %i/lib %i/admin %i/java %i/demo %i/include
cp -p instantclient*/lib* %i/lib
cp -p instantclient*/sqlplus %i/bin
cp -p instantclient*/glogin.sql %i/bin
cp -p instantclient*/*.jar %i/java
cp -p instantclient*/sdk/demo/* %i/demo
cp -p instantclient*/sdk/include/* %i/include
(cd %i/lib && ln -s libclntsh.* $(echo libclntsh.* | sed 's/[0-9.]*$//'))
