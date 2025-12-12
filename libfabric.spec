### RPM external libfabric 2.1.0
Source: https://github.com/ofiwg/%{n}/releases/download/v%{realversion}/%{n}-%{realversion}.tar.bz2
%{!?without_cuda:Requires: cuda gdrcopy}
%{!?without_rocm:Requires: rocm}
Requires: curl
Requires: numactl
Requires: rdma-core
Requires: xpmem
BuildRequires: autotools

%prep
%setup -q -n %{n}-%{realversion}

# regenerate the configure files and Makefiles
./autogen.sh

./configure \
  --prefix=%i \
  --disable-dependency-tracking \
  --disable-debug \
  --disable-profile \
  --disable-asan \
  --disable-lsan \
  --disable-tsan \
  --disable-ubsan \
  --enable-shared \
  --disable-static \
  --enable-shm \
  --enable-sm2 \
  --enable-xpmem=$XPMEM_ROOT \
  --disable-sockets \
  --enable-tcp \
  --enable-udp \
  --enable-verbs=$RDMA_CORE_ROOT \
  --disable-opx \
  --disable-psm2 \
  --disable-psm3 \
  --disable-usnic \
  --disable-efa \
  --disable-cxi \
  --disable-mrail \
  --disable-lpp \
  --disable-ucx \
  --enable-rxm \
  --enable-lnx \
%if 0%{!?without_cuda:1}
  --enable-cuda-dlopen \
  --enable-gdrcopy-dlopen \
  --with-cuda=$CUDA_ROOT \
  --with-gdrcopy=$GDRCOPY_ROOT \
%else
  --disable-cuda-dlopen \
  --disable-gdrcopy-dlopen \
  --without-cuda \
  --without-gdrcopy \
%endif
%if 0%{!?without_rocm:1}
  --enable-rocr-dlopen \
  --with-rocr=$ROCM_ROOT \
%else
  --disable-rocr-dlopen \
  --without-rocr \
%endif
  --disable-ze-dlopen \
  --without-ze \
  --with-pic \
  --with-dlopen \
  --with-gnu-ld \
  --with-curl=DIR \
  --with-numa=$NUMACTL_ROOT

  # CFLAGS="-Wno-error=array-bounds"

%build
make %{makeprocesses} 

%install
make install

%post
