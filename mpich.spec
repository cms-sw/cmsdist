### RPM external mpich v4.3.2
## INCLUDE cuda-flags
## INCLUDE rocm-flags
%define branch 4.3.x
%define tag %{realversion}
Source: git+https://github.com/pmodels/mpich.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&submodules=1&output=/%{n}-%{realversion}.tgz
BuildRequires: autotools
%{!?without_cuda:Requires: cuda}
%{!?without_rocm:Requires: rocm}
Requires: libfabric
Requires: ucx
Requires: hwloc
Requires: xpmem

# external libraries are needed for additional protocols:
#   --with-hcoll:       Mellanox Hierarchical Collectives
#   --with-pmix:        PMIx Reference Library (OpenPMIx)
# etc.

%prep
%setup -q -n %{n}-%{realversion}

# remove the submodules we do not want to use
rm -rf modules/hwloc
sed -e's/do_hwloc=.*/do_hwloc=no/' -i autogen.sh

rm -rf modules/libfabric
sed -e's/do_ofi=.*/do_ofi=no/' -i autogen.sh

rm -rf modules/ucx
sed -e's/do_ucx=.*/do_ucx=no/' -i autogen.sh

./autogen.sh

# MPICH communication device:
#   --with-device=ch4:ofi
#       should work for TCP networks and any high-bandwidth interconnect supported by libfabric.
#   --with-device=ch4:ucx
#       should work for TCP networks and any high-bandwidth interconnect supported by the UCX library.
#   --with-device=ch3
#       the legacy device ch3

# MPICH multi-threading support:
#   --enable-thread-cs={default, global, per-vci, lock-free}
#       Default is global for ch3 and per-vci for ch4
#   --enable-ch4-vci-method={default, zero, communicator, tag, implicit, explicit}
#   --enable-ch4-mt={direct, lockless, runtime}
#       direct    - Each thread directly accesses lower-level fabric (default)
#       lockless  - Use the thread safe serialization model supported by the provider
#       runtime   - Determine the model at runtime through a CVAR

# Note: using --enable-fast=O2,ndebug,alwaysinline,sse2 the compilation hangs (or takes a very long time to complete).

# For now we use build without ADM support due to an issue in the library (https://github.com/pmodels/yaksa/issues/262)
# After it's resolved, replace --without-hip with the following:

# %if 0%{!?without_rocm:1}
#   --with-hip=$ROCM_ROOT \
#   --with-hip-sm=%(echo %{rocm_archs} | sed -e's/ \+/,/g') \
# %else
#   --without-hip \
# %endif

./configure \
  --prefix=%i \
  --enable-error-checking=all \
  --enable-tag-error-bits=yes \
  --enable-fast=O2,ndebug,sse2 \
  --enable-cxx \
  --enable-romio \
  --disable-mpi-abi \
  --enable-versioning \
  --enable-threads=multiple \
  --enable-thread-cs=default \
  --disable-dependency-tracking \
  --disable-silent-rules \
  --disable-maintainer-mode \
  --enable-shared \
  --disable-static \
  --enable-nemesis-shm-collectives \
%if 0%{!?without_cuda:1}
  --with-cuda=$CUDA_ROOT \
  --with-cuda-sm=%(echo %{cuda_arch} | sed -e's/ \+/,/g') \
%else
  --without-cuda \
%endif
  --without-hip \
  --without-ze \
  --with-pic \
  --with-gnu-ld \
  --with-libfabric=$LIBFABRIC_ROOT \
  --with-ucx=$UCX_ROOT \
  --with-hwloc=$HWLOC_ROOT \
  --without-netloc \
  --with-xpmem=$XPMEM_ROOT \
  --with-yaksa=embedded \
  --with-device=ch4:ucx

%build
make %{makeprocesses} V=1

%install
make install

%post
%{relocateConfig}bin/mpicc
%{relocateConfig}bin/mpicxx
%{relocateConfig}bin/mpifort
