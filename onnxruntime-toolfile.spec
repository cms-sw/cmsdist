### RPM external onnxruntime-toolfile 0.4.0
Requires: onnxruntime
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/onnxruntime.xml
<tool name="onnxruntime" version="@TOOL_VERSION@">
  <lib name="onnxruntime"/>
  <client>
    <environment name="ONNXRUNTIME_BASE" default="@TOOL_ROOT@"/>
    <environment name="INCLUDE" default="$ONNXRUNTIME_BASE/include"/>
    <environment name="LIBDIR" default="$ONNXRUNTIME_BASE/lib64"/>
  </client>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
