### RPM external cuda 9.1.85
%define driversversion 387.26
%define cudaversion %(echo %realversion | cut -d. -f 1,2)

Source: https://developer.nvidia.com/compute/cuda/%{cudaversion}/Prod/local_installers/%{n}_%{realversion}_%{driversversion}_linux
AutoReqProv: no

%prep

%build

%install
cp %{SOURCE0} %_builddir
mkdir -p %_builddir/tmp
/bin/sh %_builddir/%{n}_%{realversion}_%{driversversion}_linux --silent --tmpdir %_builddir/tmp --extract %_builddir
# extracts:
# %_builddir/NVIDIA-Linux-x86_64-387.26.run
# %_builddir/cuda-linux.9.1.85-23083092.run
# %_builddir/cuda-samples.9.1.85-23083092-linux.run
/bin/sh %_builddir/%{n}-linux.%{realversion}-*.run -noprompt -nosymlink -tmpdir %_builddir/tmp -prefix %_builddir
ln -sf ../libnvvp/nvvp %_builddir/bin/nvvp
ln -sf ../libnsight/nsight %_builddir/bin/nsight
mkdir -p %{i}/lib64
# package only runtime and device static libraries
cp -ar %_builddir/lib64/libcudart_static.a %{i}/lib64/
cp -ar %_builddir/lib64/libcudadevrt.a %{i}/lib64/
cp -ar %_builddir/lib64/lib*_device.a %{i}/lib64/
rm -rf %_builddir/lib64/lib*.a
# do not package dynamic libraries for which we have stubs
rm -rf %_builddir/lib64/libcublas.so*
rm -rf %_builddir/lib64/libcufft.so*
rm -rf %_builddir/lib64/libcufftw.so*
rm -rf %_builddir/lib64/libcurand.so*
rm -rf %_builddir/lib64/libcusolver.so*
rm -rf %_builddir/lib64/libcusparse.so*
rm -rf %_builddir/lib64/libnpp*.so*
rm -rf %_builddir/lib64/libnvgraph.so*
rm -rf %_builddir/lib64/libnvrtc.so*
rm -rf %_builddir/lib64/libnvrtc-builtins.so*
# package the other dynamic libraries
cp -ar %_builddir/lib64/* %{i}/lib64/
cp -ar %_builddir/libnvvp %{i}
cp -ar %_builddir/libnsight %{i}
# package the includes
rm -rf %_builddir/include/sobol_direction_vectors.h
cp -ar %_builddir/include %{i}
# package the binaries and tools
cp -ar %_builddir/bin %{i}
cp -ar %_builddir/nvvm %{i}
cp -ar %_builddir/jre %{i}
