### RPM external gosamcontrib-toolfile 1.0
Requires: gosamcontrib
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/gosamcontrib.xml
<tool name="gosamcontrib" version="@TOOL_VERSION@">
  <client>
    <environment name="GOSAMCONTRIB_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$GOSAMCONTRIB_BASE/lib"/>
    <environment name="INCLUDE" default="$GOSAMCONTRIB_BASE/include"/>
  </client>
  <runtime name="GOSAMCONTRIB_PATH" value="$GOSAMCONTRIB_BASE" type="path"/>
  <runtime name="ROOT_PATH" value="$GOSAMCONTRIB_BASE" type="path"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$INCLUDE" type="path"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post

