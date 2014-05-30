### RPM external cuda-toolfile 1.0
Requires: cuda
%prep

%build

%install

mkdir -p %{i}/etc/scram.d
cat << \EOF_TOOLFILE >%{i}/etc/scram.d/cuda.xml
<tool name="cuda" version="@TOOL_VERSION@">
  <info url="https://developer.nvidia.com/cuda-toolkit"/>
  <lib name="cublas"/>
  <lib name="cublas_device"/>
  <lib name="cudadevrt"/>
  <lib name="cudart"/>
  <lib name="cudart_static"/>
  <lib name="cufft"/>
  <lib name="cufftw"/>
  <lib name="cuinj64"/>
  <lib name="curand"/>
  <lib name="cusparse"/>
  <lib name="nppc"/>
  <lib name="nppi"/>
  <lib name="npps"/>
  <lib name="nvToolsExt"/>
  <client>
    <environment name="CUDA_BASE" default="@TOOL_ROOT@/installation"/>
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
