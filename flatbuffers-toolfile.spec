### RPM external flatbuffers-toolfile 1.0
Requires: flatbuffers
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/flatbuffers.xml
<tool name="flatbuffers" version="@TOOL_VERSION@">
  <lib name="flatbuffers"/>
  <client>
    <environment name="FLATBUFFERS_BASE" default="@TOOL_ROOT@"/>
    <environment name="INCLUDE"          default="$FLATBUFFERS_BASE/include"/>
    <environment name="LIBDIR"           default="$FLATBUFFERS_BASE/lib64"/>
  </client>
  <runtime name="PATH" value="$FLATBUFFERS_BASE/bin" type="path"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
