### RPM external cuda 11.8.0
## INITENV +PATH LD_LIBRARY_PATH %i/lib64

%define runpath_opts -m compute-sanitizer -m drivers -m nvvm
%define driversversion 520.61.05

%ifarch x86_64
Source0: https://developer.download.nvidia.com/compute/cuda/%{realversion}/local_installers/%{n}_%{realversion}_%{driversversion}_linux.run
%endif
%ifarch ppc64le
Source0: https://developer.download.nvidia.com/compute/cuda/%{realversion}/local_installers/%{n}_%{realversion}_%{driversversion}_linux_ppc64le.run
%endif
%ifarch aarch64
Source0: https://developer.download.nvidia.com/compute/cuda/%{realversion}/local_installers/%{n}_%{realversion}_%{driversversion}_linux_sbsa.run
%endif
Requires: python3
AutoReq: no

%prep

%build

%install
rm -rf %_builddir/build %_builddir/tmp
mkdir %_builddir/build %_builddir/tmp

# extract and repackage the CUDA runtime
cd %_builddir/
/bin/sh %{SOURCE0} --silent --override --tmpdir=%_builddir/tmp --installpath=%_builddir/build --toolkit --keep

# create target directory structure
mkdir -p %{i}/include
mkdir -p %{i}/lib64
mkdir -p %{i}/lib64/stubs

# package only the runtime static libraries
mv %_builddir/build/lib64/libcudadevrt.a %{i}/lib64/
mv %_builddir/build/lib64/libcudart_static.a %{i}/lib64/
rm -f %_builddir/build/lib64/lib*.a

# package only the CUDA driver and NVML library stubs
mv %_builddir/build/lib64/stubs/libcuda.so      %{i}/lib64/stubs/libcuda.so
ln -sf libcuda.so                               %{i}/lib64/stubs/libcuda.so.1
mv %_builddir/build/lib64/stubs/libnvidia-ml.so %{i}/lib64/stubs/libnvidia-ml.so
ln -sf libnvidia-ml.so                          %{i}/lib64/stubs/libnvidia-ml.so.1
rm -rf %_builddir/build/lib64/stubs/

# do not package the OpenCL libraries
rm -f %_builddir/build/lib64/libOpenCL.*

# package the dynamic libraries
chmod a+x %_builddir/build/lib64/*.so
mv %_builddir/build/lib64/* %{i}/lib64/

# package the includes
chmod a-x %_builddir/build/include/*.h*
mv %_builddir/build/include/* %{i}/include/

# package the CUDA Profiling Tools Interface includes and libraries
chmod a+x %_builddir/build/extras/CUPTI/lib64/*.so*
mv %_builddir/build/extras/CUPTI/lib64/*.so* %{i}/lib64/
mv %_builddir/build/extras/CUPTI/include/*.h %{i}/include/

# leave out the Nsight and NVVP graphical tools, and package the other binaries
rm -f %_builddir/build/bin/computeprof
rm -f %_builddir/build/bin/cuda-uninstaller
rm -f %_builddir/build/bin/ncu*
rm -f %_builddir/build/bin/nsight*
rm -f %_builddir/build/bin/nsys*
rm -f %_builddir/build/bin/nv-nsight*
rm -f %_builddir/build/bin/nvvp
mv %_builddir/build/bin %{i}/

# package the cuda-gdb support files, and rename the binary to use it via a wrapper
mv %_builddir/build/share/ %{i}/
mv %{i}/bin/cuda-gdb %{i}/bin/cuda-gdb.real
cat > %{i}/bin/cuda-gdb << @EOF
#! /bin/bash
export PYTHONHOME=$PYTHON3_ROOT
exec %{i}/bin/cuda-gdb.real "\$@"
@EOF
chmod a+x %{i}/bin/cuda-gdb

# package the Compute Sanitizer, and replace the wrapper with a symlink
mv %_builddir/build/compute-sanitizer %{i}/
rm -f %{i}/bin/compute-sanitizer
ln -s ../compute-sanitizer/compute-sanitizer %{i}/bin/compute-sanitizer

# package the NVVM compiler (cicc), library (libnvvm.so), device library (libdevice.10.bc) and samples
mv %_builddir/build/nvvm %{i}/

# extract and repackage the NVIDIA libraries needed by the CUDA runtime
/bin/sh %_builddir/pkg/builds/NVIDIA-Linux-%{_arch}-%{driversversion}.run --silent --extract-only --tmpdir %_builddir/tmp --target %_builddir/build/drivers

mkdir -p %{i}/drivers
mv %_builddir/build/drivers/libcuda.so.%{driversversion}                    %{i}/drivers/
ln -sf libcuda.so.%{driversversion}                                         %{i}/drivers/libcuda.so.1
ln -sf libcuda.so.1                                                         %{i}/drivers/libcuda.so
mv %_builddir/build/drivers/libnvidia-ptxjitcompiler.so.%{driversversion}   %{i}/drivers/
ln -sf libnvidia-ptxjitcompiler.so.%{driversversion}                        %{i}/drivers/libnvidia-ptxjitcompiler.so.1
ln -sf libnvidia-ptxjitcompiler.so.1                                        %{i}/drivers/libnvidia-ptxjitcompiler.so
cp %{i}/nvvm/lib64/libnvvm.so.4.0.0                                         %{i}/drivers/
ln -sf libnvvm.so.4.0.0                                                     %{i}/drivers/libnvvm.so.4
ln -sf libnvvm.so.4                                                         %{i}/drivers/libnvvm.so

%post
# let nvcc find its components when invoked from the command line
sed \
  -e"/^TOP *=/s|= .*|= $CMS_INSTALL_PREFIX/%{pkgrel}|" \
  -e's|$(_HERE_)|$(TOP)/bin|g' \
  -e's|/$(_TARGET_DIR_)||g' \
  -e's|$(_TARGET_SIZE_)|64|g' \
  -i $RPM_INSTALL_PREFIX/%{pkgrel}/bin/nvcc.profile

# relocate the paths inside the scripts
%{relocateConfig}bin/cuda-gdb
