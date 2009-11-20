### RPM external oracle 11.2.0.1.0
## INITENV SET ORACLE_HOME %i
## BUILDIF case `uname`:`uname -p` in Linux:i*86 ) true ;; Linux:x86_64 ) true ;;  Linux:ppc64 ) false ;; Darwin:* ) false ;; * ) false ;; esac

Source0: http://cmsrep.cern.ch/cmssw/oracle-mirror/%cmsos/%realversion/oracle_lcg.tgz
Source9: oracle-license
Requires: fakesystem 

## INITENV +PATH SQLPATH %i/bin
%prep 
%setup -n %realversion

%build

%install
mkdir -p %i/bin %i/lib %i/doc %i/include
cp %_sourcedir/oracle-license %{i}/oracle-license
cp -r bin/* %i/bin/
cp -r lib/* %i/lib/
cp -r doc/* %i/doc/
cp -r include/* %i/include/

# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d

cat << \EOF_TOOLFILE >%i/etc/scram.d/%n
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=%n version=%v>
<lib name=clntsh>
<lib name=nnz11>
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

cat << \EOF_TOOLFILE >%i/etc/scram.d/oracleocci
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=oracleocci version=%v>
<lib name=occi>
<use name=oracle>
</Tool>
EOF_TOOLFILE

%post
%{relocateConfig}etc/scram.d/%n
%{relocateConfig}etc/scram.d/oracleocci
