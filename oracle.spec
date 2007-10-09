### RPM external oracle 10.2.0.3
## INITENV SET ORACLE_HOME %i
## BUILDIF case $(uname):$(uname -p) in Linux:i*86 ) true ;; Linux:x86_64 ) true ;;  Linux:ppc64 ) false ;; Darwin:* ) false ;; * ) false ;; esac

Source0: http://oraclelon1.oracle.com/otn/linux/instantclient/10201/instantclient-basic-linux32-10.2.0.2-20060331.zip
Source1: http://oraclelon1.oracle.com/otn/linux/instantclient/10201/instantclient-sdk-linux32-10.2.0.2-20060331.zip
Source2: http://oraclelon1.oracle.com/otn/linux/instantclient/10201/instantclient-sqlplus-linux32-10.2.0.2-20060331.zip

Source3: http://oraclelon1.oracle.com/otn/linux/instantclient/10201/instantclient-basic-linux-x86-64-10.2.0.2-20060228.zip
Source4: http://oraclelon1.oracle.com/otn/linux/instantclient/10201/instantclient-sdk-linux-x86-64-10.2.0.2-20060228.zip
Source5: http://oraclelon1.oracle.com/otn/linux/instantclient/10201/instantclient-sqlplus-linux-x86-64-10.2.0.2-20060228.zip

# Not accessible with a user/pass and not in suncms cache
#Source6: http://oraclelon1.oracle.com/otn/linux/instantclient/10201/instantclient-basic-macosx-10.1.0.3.zip
#Source7: http://oraclelon1.oracle.com/otn/linux/instantclient/10201/instantclient-sdk-macosx-10.1.0.3.zip
#Source8: http://oraclelon1.oracle.com/otn/linux/instantclient/10201/instantclient-sqlplus-macosx-10.1.0.3.zip

Source9: oracle-license
Source10: http://www.oracle.com/technology/tech/oci/occi/downloads/occi_gcc343_102020.tar.gz

## INITENV +PATH SQLPATH %i/bin
%prep
rm -rf instantclient_*
case %cmsos in
  slc3_ia32 )
    yes | unzip %_sourcedir/*-basic-*linux32*.zip
    yes | unzip %_sourcedir/*-sdk-*linux32*.zip
    yes | unzip %_sourcedir/*-sqlplus-*linux32*.zip
    ;;
  slc4_ia32 )
    yes | unzip %_sourcedir/*-basic-*linux32*.zip
    yes | unzip %_sourcedir/*-sdk-*linux32*.zip
    yes | unzip %_sourcedir/*-sqlplus-*linux32*.zip
    tar xzvf %_sourcedir/occi_gcc343_102020.tar.gz
    ;;
  slc*_amd64 )
    yes | unzip %_sourcedir/*-basic-*linux-x86-64*.zip
    yes | unzip %_sourcedir/*-sdk-*linux-x86-64*.zip
    yes | unzip %_sourcedir/*-sqlplus-*linux-x86-64*.zip
    ;;
  osx* )
    #yes | unzip %_sourcedir/*-basic-*macosx*.zip
    #yes | unzip %_sourcedir/*-sdk-*macosx*.zip
    #yes | unzip %_sourcedir/*-sqlplus-*macosx*.zip
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
%if "%cmsplatf" == "slc4_ia32_gcc345"
echo Copying libocci libraries for slc4_ia32_gcc345
mv libocci.so.10.1 %i/lib
mv libocci10.a %i/lib
%endif
(cd %i/lib && ln -s libclntsh.* $(echo libclntsh.* | sed 's/[0-9.]*$//'))
(cd %i/lib && ln -s libocci.* $(echo libocci.* | sed 's/[0-9.]*$//'))
chmod -R g-w %i

# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=%n version=%v>
<lib name=clntsh>
<lib name=occi>
<lib name=nnz10>
<Client>
 <Environment name=ORACLE_BASE default="%i"></Environment>
 <Environment name=ORACLE_ADMINDIR></Environment>
 <Environment name=LIBDIR value="$ORACLE_BASE/lib"></Environment>
 <Environment name=BINDIR value="$ORACLE_BASE/bin"></Environment>
 <Environment name=INCLUDE value="$ORACLE_BASE/include"></Environment>
</Client>
<use name=sockets>
<Runtime name=PATH value="$BINDIR" type=path>
<Runtime name=NLS_LANG value="american_america.WE8ISO8859P9">
<Runtime name=NLS_DATE_FORMAT value="DD-MON-FXYYYY">
<Runtime name=ORA_NLS33 default="$ORACLE_BASE/ocommon/nls/admin/data">
<Runtime name=ORACLE_HOME default="$ORACLE_BASE">
<Runtime name=TNS_ADMIN default="$ORACLE_ADMINDIR">
</Tool>
EOF_TOOLFILE

%post
%{relocateConfig}etc/scram.d/%n

