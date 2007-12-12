### RPM external oracle 11.1.0.6.0
## INITENV SET ORACLE_HOME %i
## BUILDIF case $(uname):$(uname -p) in Linux:i*86 ) true ;; Linux:x86_64 ) true ;;  Linux:ppc64 ) false ;; Darwin:* ) false ;; * ) false ;; esac

Source0: http://cmsrep.cern.ch/cmssw/oracle-mirror/%cmsos/%realversion/basic.zip
Source1: http://cmsrep.cern.ch/cmssw/oracle-mirror/%cmsos/%realversion/sdk.zip
Source2: http://cmsrep.cern.ch/cmssw/oracle-mirror/%cmsos/%realversion/sqlplus.zip
Source9: oracle-license
Source10: http://www.oracle.com/technology/tech/oci/occi/downloads/occi_gcc343_102020.tar.gz

## INITENV +PATH SQLPATH %i/bin
%prep
rm -rf instantclient_*
unzip -o -u %_sourcedir/basic.zip
unzip -o -u %_sourcedir/sdk.zip
unzip -o -u %_sourcedir/sqlplus.zip

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
[ -f libocci.so.10.1 ] && mv libocci.so.10.1 %i/lib
[ -f libocci10.a ] && mv libocci10.a %i/lib
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
