### RPM external ucx 1.21.0
## INCLUDE microarch_flags
## INCLUDE cuda-flags
Source: git+https://github.com/openucx/%{n}.git?obj=master/v%{realversion}&export=%{n}-%{realversion}&submodules=1&output=/%{n}-%{realversion}.tgz
BuildRequires: autotools
%{!?without_cuda:Requires: cuda gdrcopy}
Requires: numactl
Requires: rdma-core
%{!?without_rocm:Requires: rocm-hip rocr-runtime}
Requires: xpmem

%prep
%setup -q -n %{n}-%{realversion}

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
  --with-xpmem=$XPMEM_ROOT \
  --without-ugni \
%ifarch x86_64
  CFLAGS="%{selected_microarch}" \
  CXXFLAGS="%{selected_microarch}" \
%endif
  CPPFLAGS="-I$NUMACTL_ROOT/include" \
  LDFLAGS="-L$NUMACTL_ROOT/lib"

%build
make %{makeprocesses} V=1

%install
make install V=1

# remove pkg-config to avoid rpm-generated dependency on /usr/bin/pkg-config
rm -rf %{i}/lib/pkgconfig

# remove the libtool library files
rm -f %{i}/lib/lib*.la
rm -f %{i}/lib/ucx/lib*.la

# remove the UCX examples
rm -rf %{i}/share/ucx/examples

%post
%{relocateConfig}lib/cmake/ucx/*.cmake
