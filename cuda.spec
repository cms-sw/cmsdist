### RPM external cuda %{fullversion}

%ifarch x86_64
%define fullversion 10.0.130
%define cudaversion %(echo %realversion | cut -d. -f 1,2)
%define driversversion 410.48
%define cudasoversion %{driversversion}
%define nsightarch linux-desktop-glibc_2_11_3-glx-x64
%endif
%ifarch aarch64
%define fullversion 10.0.166
%define cudaversion %(echo %realversion | cut -d. -f 1,2)
%define driversversion 32.1.0
%define cudasoversion 1.1
%define nsightarch linux-v4l_l4t-glx-t210-a64
%endif

%ifarch x86_64
Source0: https://developer.nvidia.com/compute/cuda/%{cudaversion}/Prod/local_installers/%{n}_%{realversion}_%{driversversion}_linux
%endif
%ifarch aarch64
Source0: https://patatrack.web.cern.ch/patatrack/files/cuda-repo-l4t-10-0-local-%{realversion}_1.0-1_arm64.deb
Source1: https://patatrack.web.cern.ch/patatrack/files/Jetson_Linux_R%{driversversion}_aarch64.tbz2
%endif
AutoReq: no

%prep

%build

%install
rm -rf %_builddir/build %_builddir/tmp
mkdir %_builddir/build %_builddir/tmp
/bin/sh %{SOURCE0} --silent --tmpdir %_builddir/tmp --extract=%_builddir/build  --override

# extracts:
# %_builddir/build/NVIDIA-Linux-x86_64-410.48.run
# %_builddir/build/cuda-linux.10.0.130-24817639.run
# %_builddir/build/cuda-samples.10.0.130-24817639-linux.run

/bin/sh %_builddir/build/%{n}-linux.%{realversion}-*.run -noprompt -nosymlink -tmpdir %_builddir/tmp -prefix %_builddir/build
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
# mv the CUDA libraries to %_builddir/build
mv %_builddir/tmp/usr/local/cuda-%{cudaversion}/* %_builddir/build
%endif

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
chmod a+x %_builddir/build/lib64/*.so
chmod a+x %_builddir/build/lib64/stubs/*.so
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

# leave out the CUDA samples
rm -f %_builddir/build/bin/cuda-install-samples-%{cudaversion}.sh

# package the Nsight Compute command line tool
mkdir %{i}/NsightCompute-1.0
mv %_builddir/build/NsightCompute-1.0/target                  %{i}/NsightCompute-1.0/
%ifarch x86_64
mv %_builddir/build/NsightCompute-1.0/ProfileSectionTemplates %{i}/NsightCompute-1.0/
%endif
%ifarch aarch64
mv %_builddir/build/NsightCompute-1.0/host                    %{i}/NsightCompute-1.0/
%endif
cat > %{i}/bin/nv-nsight-cu-cli <<@EOF
#! /bin/bash
exec %{i}/NsightCompute-1.0/target/%{nsightarch}/nv-nsight-cu-cli "\$@"
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
%ifarch x86_64
/bin/sh %_builddir/build/NVIDIA-Linux-x86_64-%{driversversion}.run --accept-license --extract-only --tmpdir %_builddir/tmp --target %_builddir/build/nvidia
%endif
%ifarch aarch64
tar xaf %{SOURCE1} -C %_builddir/tmp Linux_for_Tegra/nv_tegra/nvidia_drivers.tbz2
tar xaf %_builddir/tmp/Linux_for_Tegra/nv_tegra/nvidia_drivers.tbz2 -C %_builddir/tmp usr/lib/aarch64-linux-gnu/tegra/
mv %_builddir/tmp/usr/lib/aarch64-linux-gnu/tegra %_builddir/build/nvidia
%endif
mkdir -p %{i}/drivers
mv %_builddir/build/nvidia/libcuda.so.%{cudasoversion}                    %{i}/drivers/
ln -sf libcuda.so.%{cudasoversion}                                        %{i}/drivers/libcuda.so.1
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
