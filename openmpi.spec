### RPM external openmpi 5.0.8
## INITENV SET OPAL_PREFIX %{i}
%define branch v5.0.x
%define tag v%{realversion}
Source: git+https://github.com/open-mpi/ompi.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&submodules=1&output=/%{n}-%{realversion}.tgz
BuildRequires: autotools flex
%{!?without_cuda:Requires: cuda}
Requires: libfabric
Requires: hwloc
Requires: rdma-core
Requires: xpmem
Requires: ucx
Requires: zlib

# external libraries are needed for additional protocols:
#   --with-mxm:         Mellanox Messaging (depracated, use UCX instead)
#   --with-fca:         Mellanox Fabric Collective Accelerator
#   --with-hcoll:       Mellanox Hierarchical Collectives
#   --with-knem:        High-Performance Intra-Node MPI Communication
# etc.

%prep
%setup -q -n %{n}-%{realversion}

AUTOMAKE_JOBS=%{compiling_processes} ./autogen.pl

./configure \
  --prefix=%i \
  --disable-dependency-tracking \
  --enable-ipv6 \
  --enable-shared \
  --disable-static \
  --disable-mpi-java \
  --with-zlib=$ZLIB_ROOT \
  %{!?without_cuda:--with-cuda=$CUDA_ROOT} \
  --with-hwloc=$HWLOC_ROOT \
  --with-ofi=$LIBFABRIC_ROOT \
  --without-portals4 \
  --without-psm \
  --without-psm2 \
  --with-verbs=$RDMA_CORE_ROOT \
  --without-mxm \
  --with-ucx=$UCX_ROOT \
  --with-cma \
  --without-knem \
  --with-xpmem=$XPMEM_ROOT \
  --with-pic \
  --disable-io-romio \
  --with-gnu-ld \
  --with-pmix=internal

%build
make %{makeprocesses} 

%install
make install

# remove the libtool library files
find %{i}/lib/ -name '*.la' -delete

%post
%{relocateConfig}share/openmpi/*-wrapper-data.txt
