### RPM external openmpi 4.1.1
## INITENV SET OPAL_PREFIX %{i}
Source: https://download.open-mpi.org/release/open-mpi/v4.1/%{n}-%{realversion}.tar.bz2
BuildRequires: autotools
Requires: zlib cuda hwloc ucx
# external libraries are needed for additional protocols:
#   --with-ofi:         Open Fabric Interface's libfabric
#   --with-mxm:         Mellanox Messaging
#   --with-fca:         Mellanox Fabric Collective Accelerator
#   --with-hcoll:       Mellanox Hierarchical Collectives
#   --with-lsf:         LSF job scheduler
#   --with-lustre:      Lustre filesystem
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
  --with-ucx=$UCX_ROOT \
  --without-x \
  --with-pic \
  --with-gnu-ld

%build
make %{makeprocesses} 

%install
make install

# remove the libtool library files
rm -f %{i}/lib/lib*.la
rm -f %{i}/lib/pmix/lib*.la
rm -f %{i}/lib/openmpi/lib*.la

%post
%{relocateConfig}share/openmpi/*-wrapper-data.txt
