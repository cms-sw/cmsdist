### RPM external cuda %{fullversion}

%ifarch x86_64 ppc64le
%define fullversion 10.2.89
%define cudaversion %(echo %realversion | cut -d. -f 1,2)
%define driversversion 440.33.01
%endif
%ifarch aarch64
%define fullversion 10.2.107
%define cudaversion %(echo %realversion | cut -d. -f 1,2)
%define driversversion 435.17.01
%endif

%ifarch x86_64
Source0: https://developer.download.nvidia.com/compute/cuda/%{cudaversion}/Prod/local_installers/%{n}_%{realversion}_%{driversversion}_linux.run
%endif
%ifarch ppc64le
Source0: https://developer.download.nvidia.com/compute/cuda/%{cudaversion}/Prod/local_installers/%{n}_%{realversion}_%{driversversion}_linux_ppc64le.run
%endif
%ifarch aarch64
Source0: https://patatrack.web.cern.ch/patatrack/files/cuda-repo-rhel8-10-2-local-%{realversion}-%{driversversion}-1.0-1.aarch64.rpm
%endif
Requires: python
AutoReq: no

%prep

%build

%install
rm -rf %_builddir/build %_builddir/tmp
mkdir %_builddir/build %_builddir/tmp

# extract and repackage the CUDA runtime, tools and stubs
%ifarch x86_64 ppc64le
/bin/sh %{SOURCE0} --silent --override --override-driver-check --tmpdir %_builddir/tmp --extract=%_builddir/build
# extracts:
# %_builddir/build/EULA.txt
# %_builddir/build/NVIDIA-Linux-%{_arch}-440.33.01.run  # linux drivers
# %_builddir/build/cublas/                              # standalone cuBLAS library, also included in cuda-toolkit
# %_builddir/build/cuda-samples/                        # CUDA samples
# %_builddir/build/cuda-toolkit/                        # CUDA runtime, tools and stubs
# %_builddir/build/integration/                         # scripts for running Nsight Systems and Compute

# extract NVIDIA libraries needed by the CUDA runtime to %_builddir/build/drivers
/bin/sh %_builddir/build/NVIDIA-Linux-%{_arch}-%{driversversion}.run --silent --extract-only --tmpdir %_builddir/tmp --target %_builddir/build/drivers
%endif
%ifarch aarch64
# extract the individual .rpm archives from the repository into
# %_builddir/tmp/var/cuda-repo-10-2-local-10.2.107-435.17.01/
rpm2cpio %{SOURCE0} | cpio -i -d -D %_builddir/tmp

# extract the contents from the individual .rpm archives into
# %_builddir/tmp/usr/local/cuda-10.2/...
for FILE in %_builddir/tmp/var/cuda-repo-10-2-local-%{realversion}-%{driversversion}/*.rpm; do
  rpm2cpio $FILE | cpio -i -d -D %_builddir/tmp
done
# move the CUDA libraries to %_builddir/build/cuda-toolkit/
mv %_builddir/tmp/usr/local/cuda-%{cudaversion} %_builddir/build/cuda-toolkit
mv %_builddir/tmp/usr/lib64/libcublas*          %_builddir/build/cuda-toolkit/lib64/
mv %_builddir/tmp/usr/lib64/libnvblas*          %_builddir/build/cuda-toolkit/lib64/
mv %_builddir/tmp/usr/lib64/stubs/*             %_builddir/build/cuda-toolkit/lib64/stubs/
# move the NVIDIA libraries to %_builddir/build/drivers
mv %_builddir/tmp/usr/lib64                     %_builddir/build/drivers
%endif

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
rm -f %_builddir/build/cuda-toolkit/lib64/libcusolverMg.so*
rm -f %_builddir/build/cuda-toolkit/lib64/libcusparse.so*
rm -f %_builddir/build/cuda-toolkit/lib64/libnpp*.so*
rm -f %_builddir/build/cuda-toolkit/lib64/libnvgraph.so*
rm -f %_builddir/build/cuda-toolkit/lib64/libnvidia-ml.so*
rm -f %_builddir/build/cuda-toolkit/lib64/libnvjpeg.so*
rm -f %_builddir/build/cuda-toolkit/lib64/libnvrtc.so*

# package the other dynamic libraries and the stubs
chmod a+x %_builddir/build/cuda-toolkit/lib64/*.so
chmod a+x %_builddir/build/cuda-toolkit/lib64/stubs/*.so
mv %_builddir/build/cuda-toolkit/lib64/* %{i}/lib64/

# package the includes
mv %_builddir/build/cuda-toolkit/include/* %{i}/include/

# leave out the Nsight and NVVP graphical tools
rm -f %_builddir/build/cuda-toolkit/bin/computeprof
rm -f %_builddir/build/cuda-toolkit/bin/nsight
rm -f %_builddir/build/cuda-toolkit/bin/nsight_ee_plugins_manage.sh
rm -f %_builddir/build/cuda-toolkit/bin/nv-nsight-cu-cli
rm -f %_builddir/build/cuda-toolkit/bin/nvvp

# leave out the CUDA samples
rm -f %_builddir/build/cuda-toolkit/bin/cuda-install-samples-%{cudaversion}.sh

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

# repackage the NVIDIA libraries needed by the CUDA runtime
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

# relocate the paths inside the scripts
%{relocateConfig}bin/cuda-gdb
