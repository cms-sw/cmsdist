### RPM external hwloc 2.10.0
Source: https://download.open-mpi.org/release/%{n}/v2.10/%{n}-%{realversion}.tar.bz2

BuildRequires: autotools
Requires: libpciaccess libxml2 numactl
%{!?without_rocm:Requires: rocm}
%{!?without_cuda:Requires: cuda}


%prep
%setup -n %{n}-%{realversion}

%build
./configure \
  --prefix %{i} \
  --enable-shared \
  --disable-static \
  --disable-dependency-tracking \
  --enable-cpuid \
  --enable-libxml2 \
  --disable-cairo \
  --disable-doxygen \
  --disable-opencl \
  %{!?without_cuda:--with-cuda=$CUDA_ROOT --enable-cuda --enable-nvml} \
  %{!?without_rocm:--with-rocm=$ROCM_ROOT --enable-rsmi} \
%if 0%{!?without_cuda:1}%{!?without_rocm:1}
  --enable-plugins=$(echo %{!?without_cuda:cuda,nvml,}%{!?without_rocm:rsmi} | sed 's|,$||') \
%endif
  --with-pic \
  --with-gnu-ld \
  --without-x \
  HWLOC_PCIACCESS_CFLAGS="-I$LIBPCIACCESS_ROOT/include" \
  HWLOC_PCIACCESS_LIBS="-L$LIBPCIACCESS_ROOT/lib -lpciaccess" \
  HWLOC_LIBXML2_CFLAGS="-I$LIBXML2_ROOT/include/libxml2" \
  HWLOC_LIBXML2_LIBS="-L$LIBXML2_ROOT/lib -lxml2" \
  HWLOC_NUMA_CFLAGS="-I$NUMACTL_ROOT/include" \
  HWLOC_NUMA_LIBS="-L$NUMACTL_ROOT/lib -lnuma"

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
