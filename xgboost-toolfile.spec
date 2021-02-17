### RPM external xgboost-toolfile 1.0
Requires: xgboost

%prep

%build

%install
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/xgboost.xml
<tool name="xgboost" version="@TOOL_VERSION@">
  <lib name="xgboost"/>
  <client>
    <environment name="XGBOOST_BASE" default="@TOOL_ROOT@"/>
    <environment name="BINDIR" default="$XGBOOST_BASE/bin"/>
    <environment name="LIBDIR" default="$XGBOOST_BASE/lib64"/>
    <environment name="INCLUDE" default="$XGBOOST_BASE/include"/>
  </client>
  <runtime name="PATH" value="$BINDIR" type="path"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$INCLUDE" type="path"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
