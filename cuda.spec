### RPM external cuda 10.0.130
%define driversversion 410.48
%define cudaversion %(echo %realversion | cut -d. -f 1,2)

Source0: https://developer.nvidia.com/compute/cuda/%{cudaversion}/Prod/local_installers/%{n}_%{realversion}_%{driversversion}_linux
AutoReq: no

%prep

%build

%install
rm -rf %_builddir/build %_builddir/tmp
mkdir %_builddir/build %_builddir/tmp
/bin/sh %{SOURCE0} --silent --tmpdir %_builddir/tmp --extract %_builddir/build
# extracts:
# %_builddir/build/NVIDIA-Linux-x86_64-410.48.run
# %_builddir/build/cuda-linux.10.0.130-24817639.run
# %_builddir/build/cuda-samples.10.0.130-24817639-linux.run

# extract and repackage the CUDA runtime, tools and stubs
/bin/sh %_builddir/build/%{n}-linux.%{realversion}-*.run -noprompt -nosymlink -tmpdir %_builddir/tmp -prefix %_builddir/build

# create target directory structure
mkdir -p %{i}/bin
mkdir -p %{i}/include
mkdir -p %{i}/lib64
mkdir -p %{i}/share

# package only the runtime static libraries
mv %_builddir/build/lib64/libcudart_static.a %{i}/lib64/
mv %_builddir/build/lib64/libcudadevrt.a %{i}/lib64/
rm -f %_builddir/build/lib64/lib*.a

# do not package dynamic libraries for which there are stubs
rm -f %_builddir/build/lib64/libcublas.so*
rm -f %_builddir/build/lib64/libcufft.so*
rm -f %_builddir/build/lib64/libcufftw.so*
rm -f %_builddir/build/lib64/libcurand.so*
rm -f %_builddir/build/lib64/libcusolver.so*
rm -f %_builddir/build/lib64/libcusparse.so*
rm -f %_builddir/build/lib64/libnpp*.so*
rm -f %_builddir/build/lib64/libnvgraph.so*
rm -f %_builddir/build/lib64/libnvjpeg.so*
rm -f %_builddir/build/lib64/libnvrtc.so*

# package the other dynamic libraries and the stubs
mv %_builddir/build/lib64/* %{i}/lib64/

# package the includes
rm -f %_builddir/build/include/sobol_direction_vectors.h
mv %_builddir/build/include/* %{i}/include/

# leave out the Nsight and NVVP graphical tools
#mv %_builddir/build/jre %{i}/
#mv %_builddir/build/libnsight %{i}/
#ln -sf ../libnsight/nsight %_builddir/build/bin/nsight
rm -f %_builddir/build/bin/nsight
rm -f %_builddir/build/bin/nsight_ee_plugins_manage.sh
#mv %_builddir/build/libnvvp %{i}/
#ln -sf ../libnvvp/nvvp %_builddir/build/bin/nvvp
rm -f %_builddir/build/bin/nvvp
rm -f %_builddir/build/bin/computeprof

# package the Nsight Compute command line tool
mkdir %{i}/NsightCompute-1.0
mv %_builddir/build/NsightCompute-1.0/target                  %{i}/NsightCompute-1.0/
mv %_builddir/build/NsightCompute-1.0/ProfileSectionTemplates %{i}/NsightCompute-1.0/
cat > %{i}/bin/nv-nsight-cu-cli <<@EOF
#! /bin/bash
exec %{i}/NsightCompute-1.0/target/linux-desktop-glibc_2_11_3-glx-x64/nv-nsight-cu-cli "\$@"
@EOF
chmod a+x %{i}/bin/nv-nsight-cu-cli

# package the cuda-gdb support files, and rename the binary to use it via a wrapper
mv %_builddir/build/share/gdb/ %{i}/share/
mv %_builddir/build/bin/cuda-gdb %{i}/bin/cuda-gdb.real
cat > %{i}/bin/cuda-gdb << @EOF
#! /bin/bash
export PYTHONHOME=$PYTHON_ROOT
exec %{i}/bin/cuda-gdb.real "\$@"
@EOF
chmod a+x %{i}/bin/cuda-gdb

# package the binaries and tools
mv %_builddir/build/bin/* %{i}/bin/
mv %_builddir/build/nvvm %{i}/

# package the version file
mv %_builddir/build/version.txt %{i}/

# extract and repackage the NVIDIA libraries needed by the CUDA runtime
/bin/sh %_builddir/build/NVIDIA-Linux-x86_64-%{driversversion}.run --accept-license --extract-only --tmpdir %_builddir/tmp --target %_builddir/build/nvidia
mkdir -p %{i}/drivers
mv %_builddir/build/nvidia/libcuda.so.%{driversversion}                   %{i}/drivers/
ln -sf libcuda.so.%{driversversion}                                       %{i}/drivers/libcuda.so.1
ln -sf libcuda.so.1                                                       %{i}/drivers/libcuda.so
mv %_builddir/build/nvidia/libnvidia-fatbinaryloader.so.%{driversversion} %{i}/drivers/
mv %_builddir/build/nvidia/libnvidia-ptxjitcompiler.so.%{driversversion}  %{i}/drivers/
ln -sf libnvidia-ptxjitcompiler.so.%{driversversion}                      %{i}/drivers/libnvidia-ptxjitcompiler.so.1
ln -sf libnvidia-ptxjitcompiler.so.1                                      %{i}/drivers/libnvidia-ptxjitcompiler.so

%post
# let nvcc find its components when invoked from the command line
sed \
  -e"/^TOP *=/s|= .*|= $CMS_INSTALL_PREFIX/%{pkgrel}|" \
  -e's|$(_HERE_)|$(TOP)/bin|g' \
  -e's|/$(_TARGET_DIR_)||g' \
  -e's|$(_TARGET_SIZE_)|64|g' \
  -i $RPM_INSTALL_PREFIX/%{pkgrel}/bin/nvcc.profile

# relocate the paths inside bin/nv-nsight-cu-cli
%{relocateConfig}bin/nv-nsight-cu-cli
%{relocateConfig}bin/cuda-gdb
