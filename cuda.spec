### RPM external cuda 13.4.1
## INITENV +PATH LD_LIBRARY_PATH %i/lib64

%define runpath_opts -m compute-sanitizer -m drivers -m nvvm
%define driversversion 615.71.09

%ifarch x86_64
Source0: https://developer.download.nvidia.com/compute/cuda/%{realversion}/local_installers/%{n}_%{realversion}_linux.run
Source1: https://developer.download.nvidia.com/compute/nvidia-driver/redist/nvidia_driver/linux-x86_64/nvidia_driver-linux-x86_64-%{driversversion}-archive.tar.xz
%endif
%ifarch aarch64
Source0: https://developer.download.nvidia.com/compute/cuda/%{realversion}/local_installers/%{n}_%{realversion}_linux_sbsa.run
Source1: https://developer.download.nvidia.com/compute/nvidia-driver/redist/nvidia_driver/linux-sbsa/nvidia_driver-linux-sbsa-%{driversversion}-archive.tar.xz
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

# leave out the graphical tools, and package the other binaries
rm -f %_builddir/build/bin/cuda-uninstaller
rm -f %_builddir/build/bin/ncu*
rm -f %_builddir/build/bin/nsight*
rm -f %_builddir/build/bin/nsys*
mv %_builddir/build/bin %{i}/

# package the cuda-gdb support files, and set our PYTHONHOME 
mv %_builddir/build/share/ %{i}/
sed -i '2a\
# Set PYTHONHOME\
export PYTHONHOME='$PYTHON3_ROOT'\
' %{i}/bin/cuda-gdb

# package the Compute Sanitizer, and replace the wrapper with a symlink
mv %_builddir/build/compute-sanitizer %{i}/
rm -f %{i}/bin/compute-sanitizer
ln -s ../compute-sanitizer/compute-sanitizer %{i}/bin/compute-sanitizer

# package the NVVM compiler (cicc), library (libnvvm.so), device library (libdevice.10.bc) and samples
mv %_builddir/build/nvvm %{i}/

# extract and repackage the redistributable NVIDIA driver libraries needed by the CUDA runtime
mkdir -p %_builddir/nvidia-driver
tar xaf %{SOURCE1} --directory=%_builddir/nvidia-driver --strip-components=1

mkdir -p %{i}/drivers
# libcuda.so
cp -p %_builddir/nvidia-driver/lib/libcuda.so.%{driversversion}                     %{i}/drivers/
ln -sf libcuda.so.%{driversversion}                                                 %{i}/drivers/libcuda.so.1
ln -sf libcuda.so.1                                                                 %{i}/drivers/libcuda.so
# libcudadebugger.so
cp -p %_builddir/nvidia-driver/lib/libcudadebugger.so.%{driversversion}             %{i}/drivers/
ln -sf libcudadebugger.so.%{driversversion}                                         %{i}/drivers/libcudadebugger.so.1
ln -sf libcudadebugger.so.1                                                         %{i}/drivers/libcudadebugger.so
# libnvidia-gpucomp.so
cp -p %_builddir/nvidia-driver/lib/libnvidia-gpucomp.so.%{driversversion}           %{i}/drivers/
ln -sf libnvidia-gpucomp.so.%{driversversion}                                       %{i}/drivers/libnvidia-gpucomp.so
# libnvidia-nvvm.so
cp -p %_builddir/nvidia-driver/lib/libnvidia-nvvm.so.%{driversversion}              %{i}/drivers/
ln -sf libnvidia-nvvm.so.%{driversversion}                                          %{i}/drivers/libnvidia-nvvm.so.4
ln -sf libnvidia-nvvm.so.4                                                          %{i}/drivers/libnvidia-nvvm.so
# libnvidia-nvvm70.so
cp -p %_builddir/nvidia-driver/lib/libnvidia-nvvm70.so.4                            %{i}/drivers/
ln -sf libnvidia-nvvm70.so.4                                                        %{i}/drivers/libnvidia-nvvm70.so
# libnvidia-pkcs11.so
if [ -f %_builddir/nvidia-driver/lib/libnvidia-pkcs11.so.%{driversversion} ]; then
  cp -p %_builddir/nvidia-driver/lib/libnvidia-pkcs11.so.%{driversversion}          %{i}/drivers/
  ln -sf libnvidia-pkcs11.so.%{driversversion}                                      %{i}/drivers/libnvidia-pkcs11.so
fi
# libnvidia-pkcs11-openssl3.so
if [ -f %_builddir/nvidia-driver/lib/libnvidia-pkcs11-openssl3.so.%{driversversion} ]; then
  cp -p %_builddir/nvidia-driver/lib/libnvidia-pkcs11-openssl3.so.%{driversversion} %{i}/drivers/
  ln -sf libnvidia-pkcs11-openssl3.so.%{driversversion}                             %{i}/drivers/libnvidia-pkcs11-openssl3.so
fi
# libnvidia-ptxjitcompiler.so
cp -p %_builddir/nvidia-driver/lib/libnvidia-ptxjitcompiler.so.%{driversversion}    %{i}/drivers/
ln -sf libnvidia-ptxjitcompiler.so.%{driversversion}                                %{i}/drivers/libnvidia-ptxjitcompiler.so.1
ln -sf libnvidia-ptxjitcompiler.so.1                                                %{i}/drivers/libnvidia-ptxjitcompiler.so
# libnvidia-tileiras.so
cp -p %_builddir/nvidia-driver/lib/libnvidia-tileiras.so.%{driversversion}          %{i}/drivers/
# nvidia-smi
cp -p %_builddir/nvidia-driver/sbin/nvidia-smi                                      %{i}/drivers/

# reuse the redistributable CUDA driver library and NVML library in place of the CUDA stub libraries
mkdir -p %{i}/lib64/stubs
cp -p %_builddir/nvidia-driver/lib/libcuda.so.%{driversversion}                     %{i}/lib64/stubs/
ln -sf libcuda.so.%{driversversion}                                                 %{i}/lib64/stubs/libcuda.so.1
ln -sf libcuda.so.1                                                                 %{i}/lib64/stubs/libcuda.so
cp -p %_builddir/nvidia-driver/lib/libcudadebugger.so.%{driversversion}             %{i}/lib64/stubs/
ln -sf libcudadebugger.so.%{driversversion}                                         %{i}/lib64/stubs/libcudadebugger.so.1
ln -sf libcudadebugger.so.1                                                         %{i}/lib64/stubs/libcudadebugger.so
cp -p %_builddir/nvidia-driver/lib/libnvidia-ml.so.%{driversversion}                %{i}/lib64/stubs/
ln -sf libnvidia-ml.so.%{driversversion}                                            %{i}/lib64/stubs/libnvidia-ml.so.1
ln -sf libnvidia-ml.so.1                                                            %{i}/lib64/stubs/libnvidia-ml.so

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
