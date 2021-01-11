### RPM external ucx 1.9.0
Source: https://github.com/openucx/%{n}/releases/download/v%{realversion}/%{n}-%{realversion}.tar.gz
BuildRequires: autotools
Requires: numactl cuda
%ifnarch aarch64
Requires: gdrcopy
%endif
AutoReq: no
# external libraries are needed for additional protocols:
#   --with-rocm:        AMD ROCm platform for accelerated compute
#   --with-verbs:       Verbs library for direct userspace use of RDMA (InfiniBand/iWARP) hardware
#   --with-cm:          Userspace InfiniBand Communication Managment library
#   --with-rdmacm:      Userspace RDMA Connection Manager
#   --with-knem:        KNEM High-Performance Intra-Node MPI Communication
# etc.

%prep
%setup -q -n %{n}-%{realversion}

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
  --without-java \
  --with-cuda=$CUDA_ROOT \
  --without-rocm \
%ifarch aarch64
  --without-gdrcopy \
%else
  --with-gdrcopy=$GDRCOPY_ROOT \
%endif
  --without-verbs \
  --with-rc \
  --with-ud \
  --with-dc \
  --with-mlx5-dv \
  --with-ib-hw-tm \
  --with-dm \
  --without-cm \
  --without-rdmacm \
  --without-knem \
  --with-xpmem \
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
