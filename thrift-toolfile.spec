### RPM external thrift-toolfile 1.0
Requires: thrift
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/thrift.xml
<tool name="thrift" version="@TOOL_VERSION@">
  <lib name="thrift"/>
  <lib name="thriftz"/>
  <client>
    <environment name="THRIFT_BASE" default="@TOOL_ROOT@"/>
    <environment name="INCLUDE" default="@TOOL_ROOT@/include"/>
    <environment name="LIBDIR" default="@TOOL_ROOT@/lib"/>
  </client>
  <runtime name="PATH" value="$THRIFT_BASE/bin" type="path"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
