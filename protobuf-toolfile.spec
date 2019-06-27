### RPM external protobuf-toolfile 1.0
Requires: protobuf 
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/protobuf.xml
<tool name="protobuf" version="@TOOL_VERSION@">
  <lib name="protobuf"/>
  <client>
    <environment name="PROTOBUF_BASE" default="@TOOL_ROOT@"/>
    <environment name="INCLUDE" default="$PROTOBUF_BASE/include"/>
    <environment name="LIBDIR" default="$PROTOBUF_BASE/lib"/>
    <environment name="BINDIR" default="$PROTOBUF_BASE/bin"/>
  </client>
  <runtime name="PATH" value="$PROTOBUF_BASE/bin" type="path"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
# bla bla
