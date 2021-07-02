### RPM external triton-inference-client-toolfile 1.0
Requires: triton-inference-client

%prep

%build

%install
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/triton-inference-client.xml
<tool name="triton-inference-client" version="@TOOL_VERSION@">
  <info url="https://github.com/triton-inference-server/client"/>
  <lib name="grpcclient"/> 
  <client>
    <environment name="TRITON_INFERENCE_CLIENT_BASE" default="@TOOL_ROOT@"/>
    <environment name="INCLUDE" default="$TRITON_INFERENCE_CLIENT_BASE/include"/>
    <environment name="LIBDIR"  default="$TRITON_INFERENCE_CLIENT_BASE/lib"/>
  </client>
  <use name="triton-inference-common"/>
  <use name="protobuf"/>
  <use name="grpc"/>
  <use name="cuda"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
