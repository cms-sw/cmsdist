### RPM external cuda 9.1.85
%define driversversion 387.26
%define cudaversion %(echo %realversion | cut -d. -f 1,2)

Source: https://developer.nvidia.com/compute/cuda/%{cudaversion}/Prod/local_installers/%{n}_%{realversion}_%{driversversion}_linux
AutoReq: no

%prep

%build

%install
mkdir -p %_builddir/tmp
/bin/sh %{SOURCE0} --silent --tmpdir %_builddir/tmp --extract %_builddir
# extracts:
# %_builddir/NVIDIA-Linux-x86_64-387.26.run
# %_builddir/cuda-linux.9.1.85-23083092.run
# %_builddir/cuda-samples.9.1.85-23083092-linux.run

# extract and repackage the CUDA runtime, tools and stubs
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

# extract and repackage the NVIDIA libraries needed by the CUDA runtime
/bin/sh %_builddir/NVIDIA-Linux-x86_64-%{driversversion}.run --accept-license --extract-only --tmpdir %_builddir/tmp --target %_builddir/nvidia
mkdir -p %{i}/drivers
cp -ar %_builddir/nvidia/libcuda.so.%{driversversion}                   %{i}/drivers/
ln -sf libcuda.so.%{driversversion}                                     %{i}/drivers/libcuda.so.1
cp -ar %_builddir/nvidia/libnvidia-fatbinaryloader.so.%{driversversion} %{i}/drivers/
cp -ar %_builddir/nvidia/libnvidia-ptxjitcompiler.so.%{driversversion}  %{i}/drivers/
ln -sf libnvidia-ptxjitcompiler.so.%{driversversion}                    %{i}/drivers/libnvidia-ptxjitcompiler.so.1

%post
# let nvcc find its components when invoked from the command line
cat > $RPM_INSTALL_PREFIX/%{pkgrel}/bin/nvcc.profile << @EOF

TOP              = $CMS_INSTALL_PREFIX/%{pkgrel}

NVVMIR_LIBRARY_DIR = \$(TOP)/nvvm/libdevice

LD_LIBRARY_PATH += \$(TOP)/lib:
PATH            += \$(TOP)/nvvm/bin:\$(TOP)/bin:

INCLUDES        +=  "-I\$(TOP)/include" \$(_SPACE_)

LIBRARIES        =+ \$(_SPACE_) "-L\$(TOP)/lib\$(_TARGET_SIZE_)/stubs" "-L\$(TOP)/lib\$(_TARGET_SIZE_)"

CUDAFE_FLAGS    +=
PTXAS_FLAGS     +=
@EOF
