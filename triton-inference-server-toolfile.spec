### RPM external triton-inference-server-toolfile 1.0
Requires: triton-inference-server

%prep

%build

%install
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/triton-inference-server.xml
<tool name="triton-inference-server" version="@TOOL_VERSION@">
  <info url="https://github.com/NVIDIA/triton-inference-server"/>
  <lib name="request"/> 
  <client>
    <environment name="TRITON_INFERENCE_SERVER_BASE" default="@TOOL_ROOT@"/>
    <environment name="INCLUDE" default="$TRITON_INFERENCE_SERVER_BASE/include"/>
    <environment name="LIBDIR"  default="$TRITON_INFERENCE_SERVER_BASE/lib"/>
  </client>
  <use name="protobuf"/>
  <use name="opencv"/>
  <use name="grpc"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
