### RPM external cuda 10.1.105
%define driversversion 418.39
%define cudaversion %(echo %realversion | cut -d. -f 1,2)

Source0: https://developer.nvidia.com/compute/cuda/%{cudaversion}/Prod/local_installers/%{n}_%{realversion}_%{driversversion}_linux.run
AutoReq: no

%prep

%build

%install
rm -rf %_builddir/build %_builddir/tmp
mkdir %_builddir/build %_builddir/tmp
/bin/sh %{SOURCE0} --silent --tmpdir %_builddir/tmp --extract=%_builddir/build
# extracts:
# %_builddir/build/EULA.txt
# %_builddir/build/NVIDIA-Linux-x86_64-418.39.run       # linux drivers
# %_builddir/build/cublas/                              # standalone cuBLAS library, also included in cuda-toolkit
# %_builddir/build/cuda-samples/                        # CUDA samples
# %_builddir/build/cuda-toolkit/                        # CUDA runtime, tools and stubs

# create target directory structure
mkdir -p %{i}/bin
mkdir -p %{i}/include
mkdir -p %{i}/lib64
mkdir -p %{i}/share

# package only the runtime static libraries
mv %_builddir/build/cuda-toolkit/lib64/libcudart_static.a %{i}/lib64/
mv %_builddir/build/cuda-toolkit/lib64/libcudadevrt.a %{i}/lib64/
rm -f %_builddir/build/cuda-toolkit/lib64/lib*.a

# do not package dynamic libraries for which there are stubs
rm -f %_builddir/build/cuda-toolkit/lib64/libcublas.so*
rm -f %_builddir/build/cuda-toolkit/lib64/libcublasLt.so*
rm -f %_builddir/build/cuda-toolkit/lib64/libcufft.so*
rm -f %_builddir/build/cuda-toolkit/lib64/libcufftw.so*
rm -f %_builddir/build/cuda-toolkit/lib64/libcurand.so*
rm -f %_builddir/build/cuda-toolkit/lib64/libcusolver.so*
rm -f %_builddir/build/cuda-toolkit/lib64/libcusparse.so*
rm -f %_builddir/build/cuda-toolkit/lib64/libnpp*.so*
rm -f %_builddir/build/cuda-toolkit/lib64/libnvgraph.so*
rm -f %_builddir/build/cuda-toolkit/lib64/libnvjpeg.so*
rm -f %_builddir/build/cuda-toolkit/lib64/libnvrtc.so*

# package the other dynamic libraries and the stubs
mv %_builddir/build/cuda-toolkit/lib64/* %{i}/lib64/

# package the includes
rm -f %_builddir/build/cuda-toolkit/include/sobol_direction_vectors.h
mv %_builddir/build/cuda-toolkit/include/* %{i}/include/

# leave out the Nsight and NVVP graphical tools
#rm -rf %_builddir/build/cuda-toolkit/jre
#rm -rf %_builddir/build/cuda-toolkit/libnsight
#rm -rf %_builddir/build/cuda-toolkit/libnvvp
rm -f %_builddir/build/cuda-toolkit/bin/nsight
rm -f %_builddir/build/cuda-toolkit/bin/nsight_ee_plugins_manage.sh
rm -f %_builddir/build/cuda-toolkit/bin/nvvp
rm -f %_builddir/build/cuda-toolkit/bin/computeprof

# package the Nsight Compute command line tool
mkdir %{i}/NsightCompute-2019.1
mv %_builddir/build/cuda-toolkit/NsightCompute-2019.1/target    %{i}/NsightCompute-2019.1/
mv %_builddir/build/cuda-toolkit/NsightCompute-2019.1/sections  %{i}/NsightCompute-2019.1/
cat > %{i}/bin/nv-nsight-cu-cli <<@EOF
#! /bin/bash
exec %{i}/NsightCompute-2019.1/target/linux-desktop-glibc_2_11_3-x64/nv-nsight-cu-cli "\$@"
@EOF
chmod a+x %{i}/bin/nv-nsight-cu-cli

# package the cuda-gdb support files, and rename the binary to use it via a wrapper
mv %_builddir/build/cuda-toolkit/share/gdb/ %{i}/share/
mv %_builddir/build/cuda-toolkit/bin/cuda-gdb %{i}/bin/cuda-gdb.real
cat > %{i}/bin/cuda-gdb << @EOF
#! /bin/bash
export PYTHONHOME=$PYTHON_ROOT
exec %{i}/bin/cuda-gdb.real "\$@"
@EOF
chmod a+x %{i}/bin/cuda-gdb

# package the binaries and tools
mv %_builddir/build/cuda-toolkit/bin/* %{i}/bin/
mv %_builddir/build/cuda-toolkit/nvvm %{i}/

# package the version file
mv %_builddir/build/cuda-toolkit/version.txt %{i}/

# extract and repackage the NVIDIA libraries needed by the CUDA runtime
/bin/sh %_builddir/build/NVIDIA-Linux-x86_64-%{driversversion}.run --silent --extract-only --tmpdir %_builddir/tmp --target %_builddir/build/drivers
mkdir -p %{i}/drivers
mv %_builddir/build/drivers/libcuda.so.%{driversversion}                    %{i}/drivers/
ln -sf libcuda.so.%{driversversion}                                         %{i}/drivers/libcuda.so.1
ln -sf libcuda.so.1                                                         %{i}/drivers/libcuda.so
mv %_builddir/build/drivers/libnvidia-fatbinaryloader.so.%{driversversion}  %{i}/drivers/
mv %_builddir/build/drivers/libnvidia-ptxjitcompiler.so.%{driversversion}   %{i}/drivers/
ln -sf libnvidia-ptxjitcompiler.so.%{driversversion}                        %{i}/drivers/libnvidia-ptxjitcompiler.so.1
ln -sf libnvidia-ptxjitcompiler.so.1                                        %{i}/drivers/libnvidia-ptxjitcompiler.so

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
