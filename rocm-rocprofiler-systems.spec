## INCLUDE rocm-config
### RPM external rocm-rocprofiler-systems %{rocm_version_num}
Source0: git+https://github.com/ROCm/rocm-systems.git?obj=release/rocm-rel-7.2/%{rocm_version}&export=rocm-systems&submodules=1&output=/rocm-systems.tar.gz
Source1: https://github.com/ROCm/rocm-systems/commit/6276d4d7ab8350531e84a24d3db65b9f98d85eb6.patch
Patch0: patches/rocprofiler-systems-elfutils
Requires: rocm-core rocr-runtime rocm-cmake rocprofiler roctracer hip libxml2
Requires: libunwind dyninst bz2lib
Requires: sqlite rocm-rocprofiler-sdk amdsmi zlib comgr boost tbb json py3-pybind11
BuildRequires: flex bison cmake libiberty

%prep
%setup -q -n rocm-systems
patch -p1 <%{_sourcedir}/6276d4d7ab8350531e84a24d3db65b9f98d85eb6.patch
%patch0 -p1

%build

export CPPFLAGS=-I${BZ2LIB_ROOT}/include
export LDFLAGS=-L${BZ2LIB_ROOT}/lib
cmake \
  -B %{_builddir}/build \
  -S %{_builddir}/rocm-systems/projects/rocprofiler-systems \
  -DCMAKE_INSTALL_PREFIX=%{i} \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_PREFIX_PATH="%{cmake_prefix_path};${LIBIBERTY_ROOT};${FLEX_ROOT};${BISON_ROOT}" \
  -DTBB_ROOT_DIR=${TBB_ROOT} \
  -DROCPROFSYS_USE_BFD=ON \
  -DROCPROFSYS_USE_PYTHON=ON \
  -DROCPROFSYS_BUILD_PYTHON=OFF \
  -DROCPROFSYS_BUILD_DYNINST=OFF \
  -DROCPROFSYS_BUILD_TBB=OFF \
  -DROCPROFSYS_BUILD_LIBUNWIND=OFF \
  -DROCPROFSYS_BUILD_BOOST=OFF \
  -DROCPROFSYS_BUILD_LIBIBERTY=OFF \
  -DROCPROFSYS_BUILD_ELFUTILS=ON \
  -DROCPROFILER_BUILD_SQLITE3=OFF \
  -DROCPROFSYS_BUILD_NLOHMANN_JSON=OFF \
  -DROCPROFSYS_BUILD_EXAMPLES=OFF \
  -DROCPROFSYS_BUILD_TESTING=OFF \
  -DCMAKE_FIND_DEBUG_MODE=OFF \
  -DROCPROFSYS_USE_PAPI=OFF

cmake --build %{_builddir}/build --parallel %{makeprocesses} --verbose

%install
cmake --build %{_builddir}/build --target install
