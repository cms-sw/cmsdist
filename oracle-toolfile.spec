### RPM external oracle-toolfile 2.0
Requires: oracle
%prep

%build

%install

mkdir -p %i/etc/scram.d

cat << \EOF_TOOLFILE >%i/etc/scram.d/oracle.xml
<tool name="oracle" version="@TOOL_VERSION@">
  <lib name="clntsh"/>
  @OS_LIBS@
  <client>
    <environment name="ORACLE_BASE" default="@TOOL_ROOT@"/>
    <environment name="ORACLE_ADMINDIR" value="@ORACLE_ENV_ROOT@/etc"/>
    <environment name="LIBDIR" value="$ORACLE_BASE/lib"/>
    <environment name="BINDIR" value="$ORACLE_BASE/bin"/>
    <environment name="INCLUDE" value="$ORACLE_BASE/include"/>
  </client>
  <runtime name="PATH" value="$BINDIR" type="path"/>
  <runtime name="TNS_ADMIN" default="$ORACLE_ADMINDIR"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
  <use name="sockets"/>
</tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%i/etc/scram.d/oracleocci.xml
<tool name="oracleocci" version="@TOOL_VERSION@">
  <lib name="occi"/>
  <use name="oracle"/>
</tool>
EOF_TOOLFILE

export ORACLE_ENV_ROOT
## IMPORT scram-tools-post
# bla bla
