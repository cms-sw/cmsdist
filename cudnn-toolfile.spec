### RPM external cudnn-toolfile 1.0
Requires: cudnn
%prep

%build

%install
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/cudnn.xml
<tool name="cudnn" version="@TOOL_VERSION@">
  <info url="https://docs.nvidia.com/deeplearning/cudnn/index.html"/>
  <lib name="cudnn"/>
  <client>
    <environment name="CUDNN_BASE" default="@TOOL_ROOT@"/>
    <environment name="INCLUDE" default="$CUDNN_BASE/include"/>
    <environment name="LIBDIR" default="$CUDNN_BASE/lib64"/>
  </client>
  <use name="cuda"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
