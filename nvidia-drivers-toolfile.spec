### RPM external nvidia-drivers-toolfile 1.0
Requires: nvidia-drivers
%prep

%build

%install

mkdir -p %{i}/etc/scram.d
cat << \EOF_TOOLFILE >%{i}/etc/scram.d/nvidia-drivers.xml
<tool name="nvidia-drivers" version="@TOOL_VERSION@">
  <info url="https://docs.nvidia.com/cuda/index.html"/>
  <client>
    <environment name="NVIDIA_DRIVERS_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR"              default="$NVIDIA_DRIVERS_BASE/lib64"/>
  </client>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
