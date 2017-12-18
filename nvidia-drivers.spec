### RPM external nvidia-drivers 387.26
%define cudarealversion 9.1.85
%define cudaversion %(echo %cudarealversion | cut -d. -f 1,2)

Source: https://developer.nvidia.com/compute/cuda/%{cudaversion}/Prod/local_installers/cuda_%{cudarealversion}_%{realversion}_linux
AutoReqProv: no

%prep

%build

%install
cp %{SOURCE0} %_builddir
mkdir -p %_builddir/tmp
/bin/sh %_builddir/cuda_%{cudarealversion}_%{realversion}_linux --silent --tmpdir %_builddir/tmp --extract %_builddir
# extracts:
# %_builddir/NVIDIA-Linux-x86_64-387.26.run
# %_builddir/cuda-linux.9.1.85-23083092.run
# %_builddir/cuda-samples.9.1.85-23083092-linux.run
/bin/sh %_builddir/NVIDIA-Linux-x86_64-%{realversion}.run --accept-license --extract-only --tmpdir %_builddir/tmp --target %_builddir/nvidia

mkdir -p %{i}/lib64
# NVIDIA drivers and CUDA library
cp -ar %_builddir/nvidia/libcuda.so.%{realversion}                      %{i}/lib64/
ln -sf libcuda.so.%{realversion}                                        %{i}/lib64/libcuda.so.1
cp -ar %_builddir/nvidia/libnvidia-fatbinaryloader.so.%{realversion}    %{i}/lib64/
cp -ar %_builddir/nvidia/libnvidia-ptxjitcompiler.so.%{realversion}     %{i}/lib64/
ln -sf libnvidia-ptxjitcompiler.so.%{realversion}                       %{i}/lib64/libnvidia-ptxjitcompiler.so.1
