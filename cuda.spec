### RPM external cuda 7.0.28
## NOCOMPILER

Source: http://developer.download.nvidia.com/compute/cuda/7_0/Prod/local_installers/%{n}_%{realversion}_linux.run

Provides: libc.so.6(GLIBC_2.0)
Provides: libc.so.6(GLIBC_2.1)
Provides: libc.so.6(GLIBC_2.1.3)
Provides: libc.so.6(GLIBC_2.2)
Provides: libc.so.6(GLIBC_2.3)
Provides: libc.so.6(GLIBC_2.3.2)
Provides: libc.so.6(GLIBC_2.3.3)
Provides: libdl.so.2(GLIBC_2.0)
Provides: libdl.so.2(GLIBC_2.1)
Provides: libpthread.so.0(GLIBC_2.0)
Provides: libpthread.so.0(GLIBC_2.1)
Provides: libpthread.so.0(GLIBC_2.2)
Provides: librt.so.1(GLIBC_2.2)
%prep

%build

%install
cp %{SOURCE0} %_builddir
mkdir -p %_builddir/tmp
/bin/sh %_builddir/%{n}_%{realversion}_linux.run --silent -tmpdir %_builddir/tmp --extract=%_builddir
/bin/sh %_builddir/%{n}-linux64-rel-%{realversion}-*.run -noprompt -nosymlink -prefix=%_builddir
/bin/sh %_builddir/NVIDIA-Linux-x86_64-*.run --extract-only --accept-license
cp `find %_builddir/NVIDIA-Linux-x86_64-* -maxdepth 1 -type f -name "libcuda.so*"` %_builddir/lib64
ln -sf `find %_builddir/lib64 -maxdepth 1 -type f -name "libcuda.so.*" | xargs basename` %_builddir/lib64/libcuda.so.1
rm -rf %_builddir/lib64/*.a
rm -rf %_builddir/lib64/libnppi.so* %_builddir/lib64/libcufft.so* %_builddir/lib64/libcurand.so* %_builddir/lib64/libcusparse.so* %_builddir/lib64/libcusolver.so* %_builddir/lib64/libcublas.so* %_builddir/lib64/libnvrtc-builtins.so* %_builddir/lib64/libnvrtc.so* %_builddir/lib64/libnpps.so* %_builddir/lib64/libcuinj64.so* %_builddir/lib64/libnvblas.so* %_builddir/lib64/libcufftw.so*
rm -rf %_builddir/include/sobol_direction_vectors.h %_builddir/include/nppi* %_builddir/include/curand*
cp -r %_builddir/bin %{i}
cp -r %_builddir/include %{i}
cp -r %_builddir/lib %{i}
cp -r %_builddir/lib64 %{i}
cp -r %_builddir/nvvm %{i}
