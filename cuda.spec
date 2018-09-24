### RPM external cuda 10.0.130
%define driversversion 410.48
%define cudaversion %(echo %realversion | cut -d. -f 1,2)

Source0: https://developer.nvidia.com/compute/cuda/%{cudaversion}/Prod/local_installers/%{n}_%{realversion}_%{driversversion}_linux
AutoReq: no

%prep

%build

%install
mkdir -p %_builddir/tmp
/bin/sh %{SOURCE0} --silent --tmpdir %_builddir/tmp --extract %_builddir
# extracts:
# %_builddir/NVIDIA-Linux-x86_64-410.48.run
# %_builddir/cuda-linux.10.0.130-24817639.run
# %_builddir/cuda-samples.10.0.130-24817639-linux.run

# extract and repackage the CUDA runtime, tools and stubs
/bin/sh %_builddir/%{n}-linux.%{realversion}-*.run -noprompt -nosymlink -tmpdir %_builddir/tmp -prefix %_builddir

mkdir -p %{i}/lib64
mkdir -p %{i}/bin

# package only the runtime static libraries
cp -ar %_builddir/lib64/libcudart_static.a %{i}/lib64/
cp -ar %_builddir/lib64/libcudadevrt.a %{i}/lib64/
rm -f %_builddir/lib64/lib*.a

# do not package dynamic libraries for which there are stubs
rm -f %_builddir/lib64/libcublas.so*
rm -f %_builddir/lib64/libcufft.so*
rm -f %_builddir/lib64/libcufftw.so*
rm -f %_builddir/lib64/libcurand.so*
rm -f %_builddir/lib64/libcusolver.so*
rm -f %_builddir/lib64/libcusparse.so*
rm -f %_builddir/lib64/libnpp*.so*
rm -f %_builddir/lib64/libnvgraph.so*
rm -f %_builddir/lib64/libnvjpeg.so*
rm -f %_builddir/lib64/libnvrtc.so*

# package the other dynamic libraries
cp -ar %_builddir/lib64/* %{i}/lib64/

# package the includes
rm -f %_builddir/include/sobol_direction_vectors.h
cp -ar %_builddir/include/ %{i}

# leave out the Nsight and NVVP graphical tools
#cp -ar %_builddir/jre %{i}
#cp -ar %_builddir/libnsight %{i}
#ln -sf ../libnsight/nsight %_builddir/bin/nsight
rm -f %_builddir/bin/nsight
rm -f %_builddir/bin/nsight_ee_plugins_manage.sh
#cp -ar %_builddir/libnvvp %{i}
#ln -sf ../libnvvp/nvvp %_builddir/bin/nvvp
rm -f %_builddir/bin/nvvp
rm -f %_builddir/bin/computeprof

# package the cuda-gdb support files, and rename the binary to use it via a wrapper
mkdir %{i}/share
cp -ar %_builddir/share/gdb/ %{i}/share/
mv %_builddir/bin/cuda-gdb %_builddir/bin/cuda-gdb.real

# package the binaries and tools
cp -ar %_builddir/bin/* %{i}
cp -ar %_builddir/nvvm %{i}

# package the Nsight Compute command line tool
cp -ar %_builddir/NsightCompute-1.0/target/linux-desktop-glibc_2_11_3-glx-x64/* %{i}/bin/

# package the version file
cp -ar %_builddir/version.txt %{i}

# extract and repackage the NVIDIA libraries needed by the CUDA runtime
/bin/sh %_builddir/NVIDIA-Linux-x86_64-%{driversversion}.run --accept-license --extract-only --tmpdir %_builddir/tmp --target %_builddir/nvidia
mkdir -p %{i}/drivers
cp -ar %_builddir/nvidia/libcuda.so.%{driversversion}                   %{i}/drivers/
ln -sf libcuda.so.%{driversversion}                                     %{i}/drivers/libcuda.so.1
ln -sf libcuda.so.1                                                     %{i}/drivers/libcuda.so
cp -ar %_builddir/nvidia/libnvidia-fatbinaryloader.so.%{driversversion} %{i}/drivers/
cp -ar %_builddir/nvidia/libnvidia-ptxjitcompiler.so.%{driversversion}  %{i}/drivers/
ln -sf libnvidia-ptxjitcompiler.so.%{driversversion}                    %{i}/drivers/libnvidia-ptxjitcompiler.so.1
ln -sf libnvidia-ptxjitcompiler.so.1                                    %{i}/drivers/libnvidia-ptxjitcompiler.so

%post
# let nvcc find its components when invoked from the command line
sed \
  -e"/^TOP *=/s|= .*|= $CMS_INSTALL_PREFIX/%{pkgrel}|" \
  -e's|$(_HERE_)|$(TOP)/bin|g' \
  -e's|/$(_TARGET_DIR_)||g' \
  -e's|$(_TARGET_SIZE_)|64|g' \
  -i $RPM_INSTALL_PREFIX/%{pkgrel}/bin/nvcc.profile
