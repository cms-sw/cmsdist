### RPM external pool-toolfile 1.0
Requires: pool
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/pool.xml
<tool name="pool" version="@TOOL_VERSION@" type="scram">
  <client>
    <environment name="POOL_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$POOL_BASE/$SCRAM_ARCH/lib"/>
    <environment name="POOL_BINDIR" default="$POOL_BASE/$SCRAM_ARCH/bin"/>
    <environment name="INCLUDE" default="$POOL_BASE/include"/>
  </client>
  <runtime name="PATH"                         value="$POOL_BINDIR" type="path"/>
  <runtime name="PYTHONPATH"                   value="$POOL_BINDIR" type="path"/>
  <runtime name="PYTHONPATH"                   value="$LIBDIR" type="path"/>
  <runtime name="POOL_OUTMSG_LEVEL"            value="4"/>
  <runtime name="POOL_STORAGESVC_DB_AGE_LIMIT" value="10"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
