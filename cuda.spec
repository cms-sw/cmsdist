### RPM external cuda 8.0.61

Source: https://developer.nvidia.com/compute/cuda/8.0/Prod2/local_installers/%{n}_%{realversion}_375.26_linux-run
AutoReqProv: no

%prep

%build

%install
cp %{SOURCE0} %_builddir
mkdir -p %_builddir/tmp
/bin/sh %_builddir/%{n}_%{realversion}_375.26_linux-run --silent --tmpdir %_builddir/tmp --extract %_builddir
/bin/sh %_builddir/%{n}-linux64-rel-%{realversion}-*.run -noprompt -nosymlink -tmpdir %_builddir/tmp -prefix %_builddir
/bin/sh %_builddir/NVIDIA-Linux-x86_64-*.run --accept-license --extract-only --target %_builddir/drivers
cp %_builddir/drivers/libcuda.so.* %_builddir/drivers/libnvidia-fatbinaryloader.so.* %_builddir/lib64
ln -sf `basename %_builddir/lib64/libcuda.so.*` %_builddir/lib64/libcuda.so.1
ln -sf libcuda.so.1 %_builddir/lib64/libcuda.so
ln -sf ../libnvvp/nvvp %_builddir/bin/nvvp
ln -sf ../libnsight/nsight %_builddir/bin/nsight
rm -rf %_builddir/lib64/*.a
rm -rf %_builddir/lib64/libnppi.so* %_builddir/lib64/libcufft.so* %_builddir/lib64/libcurand.so* %_builddir/lib64/libcusparse.so* %_builddir/lib64/libcusolver.so* %_builddir/lib64/libcublas.so* %_builddir/lib64/libnvrtc-builtins.so* %_builddir/lib64/libnvrtc.so* %_builddir/lib64/libnpps.so* %_builddir/lib64/libnvblas.so* %_builddir/lib64/libcufftw.so*
rm -rf %_builddir/include/sobol_direction_vectors.h %_builddir/include/nppi* %_builddir/include/curand*
cp -ar %_builddir/bin %{i}
cp -ar %_builddir/include %{i}
cp -ar %_builddir/lib64 %{i}
cp -ar %_builddir/nvvm %{i}
cp -ar %_builddir/jre %{i}
cp -ar %_builddir/libnvvp %{i}
cp -ar %_builddir/libnsight %{i}
