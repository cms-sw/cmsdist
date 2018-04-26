### RPM external cuda 9.1.85
%define driversversion 387.26
%define cudaversion %(echo %realversion | cut -d. -f 1,2)

Source0: https://developer.nvidia.com/compute/cuda/%{cudaversion}/Prod/local_installers/%{n}_%{realversion}_%{driversversion}_linux
Source1: https://developer.nvidia.com/compute/cuda/%{cudaversion}/Prod/patches/1/%{n}_%{realversion}.1_linux
Source2: https://developer.nvidia.com/compute/cuda/%{cudaversion}/Prod/patches/2/%{n}_%{realversion}.2_linux
Source3: https://developer.nvidia.com/compute/cuda/%{cudaversion}/Prod/patches/3/%{n}_%{realversion}.3_linux
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

# Patch 1 (Released Jan 25, 2018)
# cuBLAS Patch Update: This update to CUDA 9.1 includes new GEMM kernels optimized for the Volta architecture and
# improved heuristics to select GEMM kernels for given input sizes.
/bin/sh %{SOURCE1} --silent --accept-eula --tmpdir %_builddir/tmp --installdir %_builddir
rm -rf %_builddir/lib64/libcublas.so.9.1.85
rm -rf %_builddir/lib64/libnvblas.so.9.1.85

# Patch 2 (Released Feb 27, 2018)
# CUDA Compiler Patch Update: This update to CUDA 9.1 includes a bug fix to the PTX assembler (ptxas). The fix
# resolves an issue when compiling code that performs address calculations using large immediate operands.
/bin/sh %{SOURCE2} --silent --accept-eula --tmpdir %_builddir/tmp --installdir %_builddir

# Patch 3 (Released Mar 5, 2018)
# cuBLAS Patch: This CUDA 9.1 patch includes fixes to GEMM optimizations for convolutional sequence to sequence
# (seq2seq) models.
/bin/sh %{SOURCE3} --silent --accept-eula --tmpdir %_builddir/tmp --installdir %_builddir
rm -rf %_builddir/lib64/libcublas.so.9.1.128
rm -rf %_builddir/lib64/libnvblas.so.9.1.128

# patch the extracted files
patch -d%_builddir -p1 <<@EOF
diff -u a/include/crt/host_config.h b/include/crt/host_config.h
--- a/include/crt/host_config.h
+++ b/include/crt/host_config.h
@@ -116,11 +116,11 @@
 
 #if defined(__GNUC__)
 
-#if __GNUC__ > 6
+#if __GNUC__ > 7
 
-#error -- unsupported GNU version! gcc versions later than 6 are not supported!
+#error -- unsupported GNU version! gcc versions later than 7 are not supported!
 
-#endif /* __GNUC__ > 6 */
+#endif /* __GNUC__ > 7 */
 
 #if defined(__APPLE__) && defined(__MACH__) && !defined(__clang__)
 #error -- clang and clang++ are the only supported host compilers on Mac OS X!
@EOF

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
# package the version file
cp -ar %_builddir/version.txt %{i}

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
sed \
  -e"/^TOP *=/s|= .*|= $CMS_INSTALL_PREFIX/%{pkgrel}|" \
  -e's|$(_HERE_)|$(TOP)/bin|g' \
  -e's|/$(_TARGET_DIR_)||g' \
  -e's|$(_TARGET_SIZE_)|64|g' \
  -i $RPM_INSTALL_PREFIX/%{pkgrel}/bin/nvcc.profile

