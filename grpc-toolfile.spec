### RPM external grpc-toolfile 1.0
Requires: grpc

%prep

%build

%install
mkdir -p %i/etc/scram.d

cat << \EOF_TOOLFILE >%i/etc/scram.d/grpc.xml
<tool name="grpc" version="@TOOL_VERSION@">
  <info url="https://github.com/grpc/grpc"/>
  <lib name="grpc"/>
  <lib name="grpc++"/>
  <lib name="grpc++_reflection"/>
  <client>
    <environment name="GRPC_BASE" default="@TOOL_ROOT@"/>
    <environment name="INCLUDE" default="$GRPC_BASE/include"/>
    <environment name="LIBDIR" default="$GRPC_BASE/lib"/>
  </client>
  <use name="protobuf"/>
  <use name="openssl"/>
  <use name="pcre"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
