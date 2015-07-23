### RPM external cuda-toolfile 1.0
Requires: cuda
%prep

%build

%install

mkdir -p %{i}/etc/scram.d
cat << \EOF_TOOLFILE >%{i}/etc/scram.d/cuda.xml
<tool name="cuda" version="@TOOL_VERSION@">
  <info url="https://developer.nvidia.com/cuda-toolkit"/>
  <lib name="cudart"/>
  <lib name="nppc"/>
  <lib name="nvToolsExt"/>
  <client>
    <environment name="CUDA_BASE" default="@TOOL_ROOT@"/>
    <environment name="NVCC"      default="$CUDA_BASE/bin/nvcc"/>
    <environment name="BINDIR"    default="$CUDA_BASE/bin"/>
    <environment name="LIBDIR"    default="$CUDA_BASE/lib64"/>
    <environment name="INCLUDE"   default="$CUDA_BASE/include"/>
  </client>
  <flags CUDA_CFLAGS="-fPIC"/>
  <flags CUDA_FLAGS="-gencode arch=compute_35,code=sm_35"/>
  <runtime name="PATH" value="$CUDA_BASE/bin" type="path"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post

