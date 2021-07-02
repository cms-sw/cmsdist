### RPM external triton-inference-common-toolfile 1.0
Requires: triton-inference-common

%prep

%build

%install
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/triton-inference-common.xml
<tool name="triton-inference-common" version="@TOOL_VERSION@">
  <info url="https://github.com/triton-inference-server/common"/>
  <lib name="tritonasyncworkqueue"/>
  <lib name="tritoncommonerror"/>
  <lib name="tritontableprinter"/>
  <client>
    <environment name="TRITON_INFERENCE_COMMON_BASE" default="@TOOL_ROOT@"/>
    <environment name="INCLUDE" default="$TRITON_INFERENCE_COMMON_BASE/include"/>
    <environment name="LIBDIR"  default="$TRITON_INFERENCE_COMMON_BASE/lib"/>
  </client>
  <use name="protobuf"/>
  <use name="grpc"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
