### RPM external cuda 13.1.0
## INITENV +PATH LD_LIBRARY_PATH %i/lib64

%define runpath_opts -m compute-sanitizer -m drivers -m nvvm
%define driversversion 590.44.01

%ifarch x86_64
Source0: https://developer.download.nvidia.com/compute/cuda/%{realversion}/local_installers/%{n}_%{realversion}_%{driversversion}_linux.run
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
touch /tmp/cuda-installer.log
/bin/sh %{SOURCE0} --silent --override --tmpdir=%_builddir/tmp --installpath=%_builddir/build --toolkit --keep
rm -f /tmp/cuda-installer.log

# create target directory structure
mkdir -p %{i}/include
mkdir -p %{i}/lib64

# package only the runtime static libraries
mv %_builddir/build/lib64/libcudadevrt.a %{i}/lib64/
mv %_builddir/build/lib64/libcudart_static.a %{i}/lib64/
rm -f %_builddir/build/lib64/lib*.a

# the stub libraries will be replaced by the redistributable driver libraries
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

# extract and repackage the redistributable NVIDIA driver libraries needed by the CUDA runtime
/bin/sh %_builddir/pkg/builds/NVIDIA-Linux-%{_arch}-%{driversversion}.run --silent --extract-only --tmpdir %_builddir/tmp --target %_builddir/build/drivers

mkdir -p %{i}/drivers
cp -p %_builddir/build/drivers/libcuda.so.%{driversversion}                     %{i}/drivers/
ln -sf libcuda.so.%{driversversion}                                             %{i}/drivers/libcuda.so.1
ln -sf libcuda.so.1                                                             %{i}/drivers/libcuda.so
cp -p %_builddir/build/drivers/libcudadebugger.so.%{driversversion}             %{i}/drivers/
ln -sf libcudadebugger.so.%{driversversion}                                     %{i}/drivers/libcudadebugger.so.1
ln -sf libcudadebugger.so.1                                                     %{i}/drivers/libcudadebugger.so
cp -p %_builddir/build/drivers/libnvidia-ptxjitcompiler.so.%{driversversion}    %{i}/drivers/
ln -sf libnvidia-ptxjitcompiler.so.%{driversversion}                            %{i}/drivers/libnvidia-ptxjitcompiler.so.1
ln -sf libnvidia-ptxjitcompiler.so.1                                            %{i}/drivers/libnvidia-ptxjitcompiler.so
cp -p %_builddir/build/drivers/libnvidia-nvvm.so.%{driversversion}              %{i}/drivers/
ln -sf libnvidia-nvvm.so.%{driversversion}                                      %{i}/drivers/libnvidia-nvvm.so.4
ln -sf libnvidia-nvvm.so.4                                                      %{i}/drivers/libnvidia-nvvm.so
cp -p %_builddir/build/drivers/nvidia-smi                                       %{i}/drivers/

# reuse the redistributable CUDA driver library and NVML library in place of the CUDA stub libraries
mkdir -p %{i}/lib64/stubs
cp -p %_builddir/build/drivers/libcuda.so.%{driversversion}                     %{i}/lib64/stubs/
ln -sf libcuda.so.%{driversversion}                                             %{i}/lib64/stubs/libcuda.so.1
ln -sf libcuda.so.1                                                             %{i}/lib64/stubs/libcuda.so
cp -p %_builddir/build/drivers/libnvidia-ml.so.%{driversversion}                %{i}/lib64/stubs/
ln -sf libnvidia-ml.so.%{driversversion}                                        %{i}/lib64/stubs/libnvidia-ml.so.1
ln -sf libnvidia-ml.so.1                                                        %{i}/lib64/stubs/libnvidia-ml.so

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
