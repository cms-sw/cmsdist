### RPM external openmpi 4.1.4
## INITENV SET OPAL_PREFIX %{i}
Source: https://download.open-mpi.org/release/open-mpi/v4.1/%{n}-%{realversion}.tar.bz2
BuildRequires: autotools
Requires: cuda
Requires: hwloc
Requires: rdma-core
Requires: xpmem
Requires: ucx
Requires: zlib
AutoReq: no

# external libraries are needed for additional protocols:
#   --with-ofi:         Open Fabric Interface's libfabric
#   --with-mxm:         Mellanox Messaging (depracated, use UCX instead)
#   --with-fca:         Mellanox Fabric Collective Accelerator
#   --with-hcoll:       Mellanox Hierarchical Collectives
#   --with-knem:        High-Performance Intra-Node MPI Communication
# etc.

%prep
%setup -q -n %{n}-%{realversion}

./configure \
  --prefix=%i \
  --disable-dependency-tracking \
  --enable-ipv6 \
  --enable-mpi-cxx \
  --enable-shared \
  --disable-static \
  --enable-cxx-exceptions \
  --disable-mpi-java \
  --enable-openib-rdmacm-ibaddr \
  --with-zlib=$ZLIB_ROOT \
  --with-cuda=$CUDA_ROOT \
  --with-hwloc=$HWLOC_ROOT \
  --without-ofi \
  --without-portals4 \
  --without-psm \
  --without-psm2 \
  --with-verbs=$RDMA_CORE_ROOT \
  --without-mxm \
  --with-ucx=$UCX_ROOT \
  --with-cma \
  --without-knem \
  --with-xpmem=$XPMEM_ROOT \
  --without-x \
  --with-pic \
  --with-gnu-ld

%build
make %{makeprocesses} 

%install
make install

# remove the libtool library files
find %{i}/lib/ -name '*.la' -delete

%post
%{relocateConfig}share/openmpi/*-wrapper-data.txt
