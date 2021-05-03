### RPM external onnxruntime-toolfile 1.0
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
    <environment name="LIBDIR" default="$ONNXRUNTIME_BASE/lib"/>
  </client>
  <use name="protobuf"/>
%if "%{cmsos}" != "slc7_aarch64"
  <use name="cuda"/>
  <use name="cudnn"/>
%endif
  <runtime name="MLAS_DYNAMIC_CPU_ARCH" value="2"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
