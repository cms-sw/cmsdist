### RPM external cuda-toolfile 2.1
Requires: cuda
%prep

%build

%install

mkdir -p %{i}/etc/scram.d
cat << \EOF_TOOLFILE >%{i}/etc/scram.d/cuda-stubs.xml
<tool name="cuda-stubs" version="@TOOL_VERSION@">
  <info url="https://docs.nvidia.com/cuda/index.html"/>
  <lib name="cuda"/>
  <client>
    <environment name="CUDA_STUBS_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR"          default="$CUDA_STUBS_BASE/lib64/stubs"/>
    <environment name="INCLUDE"         default="$CUDA_STUBS_BASE/include"/>
  </client>
  <flags SKIP_TOOL_SYMLINKS="1"/>
</tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%{i}/etc/scram.d/cuda.xml
<tool name="cuda" version="@TOOL_VERSION@">
  <info url="https://docs.nvidia.com/cuda/index.html"/>
  <use name="cuda-stubs"/>
  <lib name="cudart"/>
  <lib name="cudadevrt"/>
  <lib name="nvToolsExt"/>
  <client>
    <environment name="CUDA_BASE" default="@TOOL_ROOT@"/>
    <environment name="NVCC"      default="$CUDA_BASE/bin/nvcc"/>
    <environment name="BINDIR"    default="$CUDA_BASE/bin"/>
    <environment name="LIBDIR"    default="$CUDA_BASE/lib64"/>
    <environment name="INCLUDE"   default="$CUDA_BASE/include"/>
  </client>
  <flags CUDA_FLAGS="-gencode arch=compute_35,code=sm_35"/>
  <flags CUDA_FLAGS="-gencode arch=compute_61,code=sm_61"/>
  <flags CUDA_FLAGS="-gencode arch=compute_70,code=sm_70"/>
  <flags CUDA_FLAGS="-O3 -std=c++14 --expt-relaxed-constexpr --expt-extended-lambda"/>
  <flags CUDA_HOST_REM_CXXFLAGS="-std=%"/>
  <flags CUDA_HOST_REM_CXXFLAGS="%potentially-evaluated-expression"/>
  <flags CUDA_HOST_CXXFLAGS="-std=c++14"/>
  <lib name="cudadevrt" type="cuda"/>
  <runtime name="PATH" value="$CUDA_BASE/bin" type="path"/>
</tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%{i}/etc/scram.d/cuda-cublas.xml
<tool name="cuda-cublas" version="@TOOL_VERSION@">
  <info url="https://docs.nvidia.com/cuda/cublas/index.html"/>
  <use name="cuda"/>
  <lib name="cublas"/>
  <lib name="cublas_device"/>
  <lib name="cublas_device" type="cuda"/>
</tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%{i}/etc/scram.d/cuda-cufft.xml
<tool name="cuda-cufft" version="@TOOL_VERSION@">
  <info url="https://docs.nvidia.com/cuda/cufft/index.html"/>
  <use name="cuda"/>
  <lib name="cufft"/>
  <lib name="cufftw"/>
</tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%{i}/etc/scram.d/cuda-curand.xml
<tool name="cuda-curand" version="@TOOL_VERSION@">
  <info url="https://docs.nvidia.com/cuda/curand/index.html"/>
  <use name="cuda"/>
  <lib name="curand"/>
</tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%{i}/etc/scram.d/cuda-cusolver.xml
<tool name="cuda-cusolver" version="@TOOL_VERSION@">
  <info url="https://docs.nvidia.com/cuda/cusolver/index.html"/>
  <use name="cuda"/>
  <lib name="cusolver"/>
</tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%{i}/etc/scram.d/cuda-cusparse.xml
<tool name="cuda-cusparse" version="@TOOL_VERSION@">
  <info url="https://docs.nvidia.com/cuda/cusparse/index.html"/>
  <use name="cuda"/>
  <lib name="cusparse"/>
</tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%{i}/etc/scram.d/cuda-npp.xml
<tool name="cuda-npp" version="@TOOL_VERSION@">
  <info url="https://docs.nvidia.com/cuda/npp/index.html"/>
  <use name="cuda"/>
  <lib name="nppial"/>
  <lib name="nppicc"/>
  <lib name="nppicom"/>
  <lib name="nppidei"/>
  <lib name="nppif"/>
  <lib name="nppig"/>
  <lib name="nppim"/>
  <lib name="nppist"/>
  <lib name="nppisu"/>
  <lib name="nppitc"/>
  <lib name="npps"/>
  <lib name="nppc"/>
</tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%{i}/etc/scram.d/cuda-nvgraph.xml
<tool name="cuda-nvgraph" version="@TOOL_VERSION@">
  <info url="https://docs.nvidia.com/cuda/nvgraph/index.html"/>
  <use name="cuda"/>
  <lib name="nvgraph"/>
</tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%{i}/etc/scram.d/cuda-nvml.xml
<tool name="cuda-nvml" version="@TOOL_VERSION@">
  <info url="https://docs.nvidia.com/deploy/nvml-api/index.html"/>
  <use name="cuda"/>
  <lib name="nvidia-ml"/>
</tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%{i}/etc/scram.d/cuda-nvrtc.xml
<tool name="cuda-nvrtc" version="@TOOL_VERSION@">
  <info url="https://docs.nvidia.com/cuda/nvrtc/index.html"/>
  <use name="cuda"/>
  <lib name="nvrtc"/>
</tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%{i}/etc/scram.d/nvidia-drivers.xml
<tool name="nvidia-drivers" version="@TOOL_VERSION@">
  <info url="https://docs.nvidia.com/cuda/index.html"/>
  <client>
    <environment name="NVIDIA_DRIVERS_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR"              default="$NVIDIA_DRIVERS_BASE/drivers"/>
  </client>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
