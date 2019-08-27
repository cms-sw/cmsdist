### RPM external cuda %{fullversion}

%ifarch x86_64
%define fullversion 10.1.168
%define cudaversion %(echo %realversion | cut -d. -f 1,2)
%define driversversion 418.67
%define cudasoversion %{driversversion}
%define nsightarch linux-desktop-glibc_2_11_3-x64
%define nsightversion 2019.3
%endif
%ifarch aarch64
%define fullversion 10.0.166
%define cudaversion %(echo %realversion | cut -d. -f 1,2)
%define driversversion 32.1.0
%define cudasoversion 1.1
%define nsightarch linux-v4l_l4t-glx-t210-a64
%define nsightversion 1.0
%endif

%ifarch x86_64
Source0: https://developer.nvidia.com/compute/cuda/%{cudaversion}/Prod/local_installers/%{n}_%{realversion}_%{driversversion}_linux.run
%endif
%ifarch aarch64
Source0: https://patatrack.web.cern.ch/patatrack/files/cuda-repo-l4t-10-0-local-%{realversion}_1.0-1_arm64.deb
Source1: https://patatrack.web.cern.ch/patatrack/files/Jetson_Linux_R%{driversversion}_aarch64.tbz2
%endif
Requires: python
AutoReq: no

%prep

%build

%install
rm -rf %_builddir/build %_builddir/tmp
mkdir %_builddir/build %_builddir/tmp

# extract and repackage the CUDA runtime, tools and stubs
%ifarch x86_64
/bin/sh %{SOURCE0} --silent --override --tmpdir %_builddir/tmp --extract=%_builddir/build
# extracts:
# %_builddir/build/EULA.txt
# %_builddir/build/NVIDIA-Linux-x86_64-418.39.run       # linux drivers
# %_builddir/build/cublas/                              # standalone cuBLAS library, also included in cuda-toolkit
# %_builddir/build/cuda-samples/                        # CUDA samples
# %_builddir/build/cuda-toolkit/                        # CUDA runtime, tools and stubs
%endif
%ifarch aarch64
# extract the individual .deb archives from the repository into
# %_builddir/tmp/var/cuda-repo-10-0-local-10.0.166/
ar p %{SOURCE0} data.tar.xz | tar xv --xz -C %_builddir/tmp

# extract the contents from the individual .deb archives into
# %_builddir/tmp/usr/local/cuda-10.0/...
for FILE in %_builddir/tmp/var/cuda-repo-10-0-local-%{realversion}/*.deb; do
  ar p $FILE data.tar.xz | tar xv --xz -C %_builddir/tmp
done
# mv the CUDA libraries to %_builddir/build/cuda-toolkit/
mv %_builddir/tmp/usr/local/cuda-%{cudaversion} %_builddir/build/cuda-toolkit
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
rm -f %_builddir/build/cuda-toolkit/lib64/libcusparse.so*
rm -f %_builddir/build/cuda-toolkit/lib64/libnpp*.so*
rm -f %_builddir/build/cuda-toolkit/lib64/libnvgraph.so*
rm -f %_builddir/build/cuda-toolkit/lib64/libnvjpeg.so*
rm -f %_builddir/build/cuda-toolkit/lib64/libnvrtc.so*

# package the other dynamic libraries and the stubs
chmod a+x %_builddir/build/cuda-toolkit/lib64/*.so
chmod a+x %_builddir/build/cuda-toolkit/lib64/stubs/*.so
mv %_builddir/build/cuda-toolkit/lib64/* %{i}/lib64/

# package the includes
rm -f %_builddir/build/cuda-toolkit/include/sobol_direction_vectors.h
mv %_builddir/build/cuda-toolkit/include/* %{i}/include/

# leave out the Nsight and NVVP graphical tools
rm -f %_builddir/build/cuda-toolkit/bin/nsight
rm -f %_builddir/build/cuda-toolkit/bin/nsight_ee_plugins_manage.sh
rm -f %_builddir/build/cuda-toolkit/bin/nvvp
rm -f %_builddir/build/cuda-toolkit/bin/computeprof

# leave out the CUDA samples
rm -f %_builddir/build/cuda-toolkit/bin/cuda-install-samples-%{cudaversion}.sh

# package the Nsight Compute command line tool
mkdir %{i}/NsightCompute
mv %_builddir/build/cuda-toolkit/NsightCompute-%{nsightversion}/target      %{i}/NsightCompute/
%ifarch x86_64
mv %_builddir/build/cuda-toolkit/NsightCompute-%{nsightversion}/sections    %{i}/NsightCompute/
%endif
%ifarch aarch64
mv %_builddir/build/cuda-toolkit/NsightCompute-%{nsightversion}/host        %{i}/NsightCompute/
%endif
cat > %{i}/bin/nv-nsight-cu-cli <<@EOF
#! /bin/bash
exec %{i}/NsightCompute/target/%{nsightarch}/nv-nsight-cu-cli "\$@"
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
%ifarch x86_64
/bin/sh %_builddir/build/NVIDIA-Linux-x86_64-%{driversversion}.run --silent --extract-only --tmpdir %_builddir/tmp --target %_builddir/build/drivers
%endif
%ifarch aarch64
tar xaf %{SOURCE1} -C %_builddir/tmp Linux_for_Tegra/nv_tegra/nvidia_drivers.tbz2
tar xaf %_builddir/tmp/Linux_for_Tegra/nv_tegra/nvidia_drivers.tbz2 -C %_builddir/tmp usr/lib/aarch64-linux-gnu/tegra/
mv %_builddir/tmp/usr/lib/aarch64-linux-gnu/tegra %_builddir/build/drivers
%endif
mkdir -p %{i}/drivers
mv %_builddir/build/drivers/libcuda.so.%{cudasoversion}                     %{i}/drivers/
ln -sf libcuda.so.%{cudasoversion}                                          %{i}/drivers/libcuda.so.1
ln -sf libcuda.so.1                                                         %{i}/drivers/libcuda.so
mv %_builddir/build/drivers/libnvidia-fatbinaryloader.so.%{driversversion}  %{i}/drivers/
mv %_builddir/build/drivers/libnvidia-ptxjitcompiler.so.%{driversversion}   %{i}/drivers/
ln -sf libnvidia-ptxjitcompiler.so.%{driversversion}                        %{i}/drivers/libnvidia-ptxjitcompiler.so.1
ln -sf libnvidia-ptxjitcompiler.so.1                                        %{i}/drivers/libnvidia-ptxjitcompiler.so
%ifarch aarch64
mv %_builddir/build/drivers/libnvrm.so                                      %{i}/drivers/
mv %_builddir/build/drivers/libnvrm_gpu.so                                  %{i}/drivers/
mv %_builddir/build/drivers/libnvrm_graphics.so                             %{i}/drivers/
mv %_builddir/build/drivers/libnvos.so                                      %{i}/drivers/
%endif

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
