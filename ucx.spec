### RPM external ucx 1.23.0
## INCLUDE microarch_flags
## INCLUDE cuda-flags
Source: git+https://github.com/openucx/%{n}.git?obj=v1.23.x/v%{realversion}&export=%{n}-%{realversion}&submodules=1&output=/%{n}-%{realversion}.tgz
Patch0: ucx-device-impl-cuda-rocm
Patch1: ucx-nvcc-verbs-include
BuildRequires: autotools libiberty
Requires: zlib
%{!?without_cuda:Requires: cuda gdrcopy}
Requires: numactl
Requires: rdma-core
%{!?without_rocm:Requires: rocm-hip rocr-runtime}
Requires: xpmem

%prep
%setup -q -n %{n}-%{realversion}
%patch0 -p1
%patch1 -p1

# regenerate the configure files and Makefiles
./autogen.sh

./configure \
  --prefix=%i \
  --enable-mt \
  --disable-logging \
  --disable-debug \
  --disable-assertions \
  --disable-params-check \
  --disable-dependency-tracking \
  --enable-openmp \
  --enable-shared \
  --disable-static \
  --enable-ucg \
  --disable-doxygen-doc \
  --disable-doxygen-man \
  --disable-doxygen-html \
  --enable-compiler-opt \
  --enable-cma \
  --with-pic \
  --with-gnu-ld \
  --without-go \
  --without-java \
%if 0%{!?without_cuda:1}
  --with-cuda=$CUDA_ROOT \
  --with-gdrcopy=$GDRCOPY_ROOT \
  --with-nvcc-gencode='%{nvcc_flags_cuda_archs}' \
%else
  --without-cuda \
  --without-gdrcopy \
%endif
%if 0%{!?without_rocm:1}
  --with-rocm=$ROCM_HIP_ROOT \
%else
  --without-rocm \
%endif
  --with-verbs=$RDMA_CORE_ROOT \
  --with-rc \
  --with-ud \
  --with-dc \
  --with-mlx5-dv \
  --with-ib-hw-tm \
  --with-dm \
  --with-rdmacm=$RDMA_CORE_ROOT \
  --without-knem \
  --with-bfd=$GCC_ROOT \
  --with-xpmem=$XPMEM_ROOT \
  --without-ugni \
%ifarch x86_64
  CFLAGS="%{selected_microarch}" \
  CXXFLAGS="%{selected_microarch}" \
%endif
  CPPFLAGS="-I$NUMACTL_ROOT/include%{!?without_rocm: -I$ROCR_RUNTIME_ROOT/include/hsa}" \
  CFLAGS="-Wno-error=deprecated-openmp" \
  CXXFLAGS="-Wno-error=deprecated-openmp" \
  LDFLAGS="-Wl,--exclude-libs,libbfd.a:libiberty.a:libsframe.a -L$LIBIBERTY_ROOT/lib -L$ZLIB_ROOT/lib -L$NUMACTL_ROOT/lib%{!?without_rocm: -L$ROCR_RUNTIME_ROOT/lib64}"

%build
make %{makeprocesses} V=1

%install
make install V=1

%if 0%{!?without_rocm:1}
# configure warns, but doesn't stop, if the ROCm support cannot be enabled.
# Check explicitly that the rocm UCT and UCM modules have been built.
test -f %{i}/lib/ucx/libuct_rocm.so
test -f %{i}/lib/ucx/libucm_rocm.so
%endif

# remove pkg-config to avoid rpm-generated dependency on /usr/bin/pkg-config
rm -rf %{i}/lib/pkgconfig

# remove the libtool library files
rm -f %{i}/lib/lib*.la
rm -f %{i}/lib/ucx/lib*.la

# remove the UCX examples
rm -rf %{i}/share/ucx/examples

%post
%{relocateConfig}lib/cmake/ucx/*.cmake
