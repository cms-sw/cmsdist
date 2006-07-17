### RPM external oracle 10.2.0.2
## INITENV SET ORACLE_HOME %i

Source0: http://oraclelon1.oracle.com/otn/linux/instantclient/10201/instantclient-basic-linux32-10.2.0.2-20060331.zip
Source1: http://oraclelon1.oracle.com/otn/linux/instantclient/10201/instantclient-sdk-linux32-10.2.0.2-20060331.zip
Source2: http://oraclelon1.oracle.com/otn/linux/instantclient/10201/instantclient-sqlplus-linux32-10.2.0.2-20060331.zip

Source3: http://oraclelon1.oracle.com/otn/linux/instantclient/10201/instantclient-basic-linux-x86-64-10.2.0.2-20060228.zip
Source4: http://oraclelon1.oracle.com/otn/linux/instantclient/10201/instantclient-sdk-linux-x86-64-10.2.0.2-20060228.zip
Source5: http://oraclelon1.oracle.com/otn/linux/instantclient/10201/instantclient-sqlplus-linux-x86-64-10.2.0.2-20060228.zip

Source6: http://oraclelon1.oracle.com/otn/linux/instantclient/10201/instantclient-basic-macosx-10.1.0.3.zip
Source7: http://oraclelon1.oracle.com/otn/linux/instantclient/10201/instantclient-sdk-macosx-10.1.0.3.zip
Source8: http://oraclelon1.oracle.com/otn/linux/instantclient/10201/instantclient-sqlplus-macosx-10.1.0.3.zip

Source9: oracle-license

## INITENV +PATH SQLPATH %i/bin
%prep
rm -rf instantclient_*
case %cmsos in
  slc*_ia32 )
    yes | unzip %_sourcedir/*-basic-*linux32*.zip
    yes | unzip %_sourcedir/*-sdk-*linux32*.zip
    yes | unzip %_sourcedir/*-sqlplus-*linux32*.zip
    ;;
  slc*_amd64 )
    yes | unzip %_sourcedir/*-basic-*linux-x86-64*.zip
    yes | unzip %_sourcedir/*-sdk-*linux-x86-64*.zip
    yes | unzip %_sourcedir/*-sqlplus-*linux-x86-64*.zip
    ;;
  osx* )
    yes | unzip %_sourcedir/*-basic-*macosx*.zip
    yes | unzip %_sourcedir/*-sdk-*macosx*.zip
    yes | unzip %_sourcedir/*-sqlplus-*macosx*.zip
    ;;  
esac

%build
%install
mkdir -p %i/bin %i/etc %i/lib %i/admin %i/java %i/demo %i/include
cp %_sourcedir/oracle-license %{i}/oracle-license
cp -p instantclient*/lib* %i/lib
cp -p instantclient*/sqlplus %i/bin
cp -p instantclient*/glogin.sql %i/bin
cp -p instantclient*/*.jar %i/java
cp -p instantclient*/sdk/demo/* %i/demo
cp -p instantclient*/sdk/include/* %i/include
(cd %i/lib && ln -s libclntsh.* $(echo libclntsh.* | sed 's/[0-9.]*$//'))
(cd %i/lib && ln -s libocci.* $(echo libocci.* | sed 's/[0-9.]*$//'))
