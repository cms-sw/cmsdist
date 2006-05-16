### RPM external oracle 10.2.0.1
## INITENV SET ORACLE_HOME %i

%define pkg0name_slc3_ia32_gcc323 instantclient-basic-linux32-10.2.0.1-20050713.zip
%define pkg1name_slc3_ia32_gcc323 instantclient-sdk-linux32-10.2.0.1-20050713.zip
%define pkg2name_slc3_ia32_gcc323 instantclient-sqlplus-linux32-10.2.0.1-20050713.zip
Source0: http://oraclelon1.oracle.com/otn/linux/instantclient/10201/%{pkg0name_slc3_ia32_gcc323}
Source1: http://oraclelon1.oracle.com/otn/linux/instantclient/10201/%{pkg1name_slc3_ia32_gcc323}
Source2: http://oraclelon1.oracle.com/otn/linux/instantclient/10201/%{pkg2name_slc3_ia32_gcc323}

%define pkg0name_slc3_amd64_gcc345 instantclient-basic-linux-x86-64-10.2.0.2-20060228.zip
%define pkg1name_slc3_amd64_gcc345 instantclient-sdk-linux-x86-64-10.2.0.2-20060228.zip
%define pkg2name_slc3_amd64_gcc345 instantclient-sqlplus-linux-x86-64-10.2.0.2-20060228.zip

Source3: http://oraclelon1.oracle.com/otn/linux/instantclient/10201/%{pkg0name_slc3_amd64_gcc345}
Source4: http://oraclelon1.oracle.com/otn/linux/instantclient/10201/%{pkg1name_slc3_amd64_gcc345}
Source5: http://oraclelon1.oracle.com/otn/linux/instantclient/10201/%{pkg2name_slc3_amd64_gcc345}

## INITENV +PATH SQLPATH %i/bin
%prep
rm -rf instantclient_$(echo %v | cut -f1,2 -d. | tr . _)
%define tmpPlatf %(echo %cmsplatf|cut -d_ -f1,2)
if [ "%tmpPlatf" == "slc3_ia32" ]
then
yes | unzip %_sourcedir/%{pkg0name_slc3_ia32_gcc323}
yes | unzip %_sourcedir/%{pkg1name_slc3_ia32_gcc323}
yes | unzip %_sourcedir/%{pkg2name_slc3_ia32_gcc323}
elif [ "%tmpPlatf" == "slc3_amd64" ]
then
yes | unzip %_sourcedir/%{pkg0name_slc3_amd64_gcc345}
yes | unzip %_sourcedir/%{pkg1name_slc3_amd64_gcc345}
yes | unzip %_sourcedir/%{pkg2name_slc3_amd64_gcc345}
fi

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
