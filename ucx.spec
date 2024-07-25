### RPM external ucx 1.17.0
Source: https://github.com/openucx/%{n}/archive/refs/tags/v%{realversion}.tar.gz
BuildRequires: autotools
%{!?without_cuda:Requires: cuda gdrcopy}
Requires: numactl
Requires: rdma-core
%{!?without_rocm:Requires: rocm}
Requires: xpmem

%prep
%setup -q -n %{n}-%{realversion}

# regenerate the configure files and Makefiles
./autogen.sh

./configure \
  --prefix=%i \
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
  --enable-mt \
  --with-pic \
  --with-gnu-ld \
  --with-avx \
  --with-sse41 \
  --with-sse42 \
  --without-go \
  --without-java \
%if 0%{!?without_cuda:1}
  --with-cuda=$CUDA_ROOT \
  --with-gdrcopy=$GDRCOPY_ROOT \
%else
  --without-cuda \
  --without-gdrcopy \
%endif
%if 0%{!?without_rocm:1}
  --with-rocm=$ROCM_ROOT \
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
  CFLAGS="-Wno-error=array-bounds" \
  CPPFLAGS="-I$NUMACTL_ROOT/include" \
  LDFLAGS="-L$NUMACTL_ROOT/lib"

%build
make %{makeprocesses} 

%install
make install

# remove pkg-config to avoid rpm-generated dependency on /usr/bin/pkg-config
rm -rf %{i}/lib/pkgconfig

# remove the libtool library files
rm -f %{i}/lib/lib*.la
rm -f %{i}/lib/ucx/lib*.la

# remove the UCX examples
rm -rf %{i}/share/ucx/examples

%post
%{relocateConfig}lib/cmake/ucx/*.cmake
