### RPM external oracle 11.2.0.1.0p1
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

cat << \EOF_TOOLFILE >%i/etc/scram.d/%n.xml
  <tool name="oracle" version="%v">
    <lib name="clntsh"/>
    <lib name="nnz11"/>
    <client>
      <environment name="ORACLE_BASE" default="%i"/>
      <environment name="ORACLE_ADMINDIR"/>
      <environment name="LIBDIR" value="$ORACLE_BASE/lib"/>
      <environment name="BINDIR" value="$ORACLE_BASE/bin"/>
      <environment name="INCLUDE" value="$ORACLE_BASE/include"/>
    </client>
    <runtime name="PATH" value="$BINDIR" type="path"/>
    <runtime name="TNS_ADMIN" default="$ORACLE_ADMINDIR"/>
    <use name="sockets"/>
  </tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%i/etc/scram.d/oracleocci.xml
  <tool name="oracleocci" version="%v">
    <lib name="occi"/>
    <use name="oracle"/>
  </tool>
EOF_TOOLFILE

%post
%{relocateConfig}etc/scram.d/%n.xml
%{relocateConfig}etc/scram.d/oracleocci.xml
