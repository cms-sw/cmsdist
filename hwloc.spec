### RPM external hwloc 2.4.0
Source: https://download.open-mpi.org/release/%{n}/v2.4/%{n}-%{realversion}.tar.bz2

BuildRequires: autotools
Requires: cuda libpciaccess libxml2 numactl

%prep
%setup -n %{n}-%{realversion}

./configure \
  --prefix %{i} \
  --enable-shared \
  --disable-static \
  --disable-dependency-tracking \
  --enable-cpuid \
  --enable-cuda \
  --enable-nvml \
  --enable-libxml2 \
  --disable-cairo \
  --disable-doxygen \
  --enable-plugins=cuda,nvml \
  --with-pic \
  --with-gnu-ld \
  --without-x \
  CPPFLAGS="-I$CUDA_ROOT/include" \
  LDFLAGS="-L$CUDA_ROOT/lib64 -L$CUDA_ROOT/lib64/stubs" \
  HWLOC_PCIACCESS_CFLAGS="-I$LIBPCIACCESS_ROOT/include" \
  HWLOC_PCIACCESS_LIBS="-L$LIBPCIACCESS_ROOT/lib -lpciaccess" \
  HWLOC_LIBXML2_CFLAGS="-I$LIBXML2_ROOT/include/libxml2" \
  HWLOC_LIBXML2_LIBS="-L$LIBXML2_ROOT/lib -lxml2" \
  HWLOC_NUMA_CFLAGS="-I$NUMACTL_ROOT/include" \
  HWLOC_NUMA_LIBS="-L$NUMACTL_ROOT/lib -lnuma"

%build
make %{makeprocesses} 

%install
make install

# remove the libtool library files
rm -f  %{i}/lib/lib*.la
rm -f  %{i}/lib/hwloc/*.la

# remove unnecessary or unwanted files
rm -rf %{i}/sbin
rm -rf %{i}/share/doc
rm -rf %{i}/share/hwloc
rm -f  %{i}/share/man/man1/hwloc-dump-hwdata.1

%post
%{relocateConfig}bin/hwloc-compress-dir
%{relocateConfig}bin/hwloc-gather-topology
