## INCLUDE rocm-config
### RPM external rocm-rocprofiler-systems %{rocm_version_num}
Patch0: patches/rocprofiler-systems-elfutils
Patch1: patches/rocprofiler-systems-dyninst-tbb-boost-conflict
Requires: rocm-core rocr-runtime rocprofiler roctracer rocm-hip libxml2
Requires: libunwind dyninst bz2lib
Requires: sqlite rocm-rocprofiler-sdk amdsmi zlib rocm-comgr boost tbb json py3-pybind11 elfutils
BuildRequires: flex bison cmake libiberty rocm-llvm rocm-cmake
%define rocm_project rocprofiler-systems
%define ROCMPostPrep patch -p3 -i %{PATCH0} ; patch -p3 -i %{PATCH1}
%define ROCMPreBuild export CPPFLAGS=-I${BZ2LIB_ROOT}/include; export LDFLAGS=-L${BZ2LIB_ROOT}/lib; export PKG_CONFIG_PATH=${ELFUTILS_ROOT}/lib/pkgconfig:/usr/lib64/pkgconfig${PKG_CONFIG_PATH:+:$PKG_CONFIG_PATH}; perl -i -0pe 's|#include <elf-bfd\\.h>\\n#include <elfutils/libdw\\.h>|#include <elfutils/libdw.h>\\n#include <elf-bfd.h>|' %{_builddir}/rocm-systems/projects/rocprofiler-systems/source/lib/binary/symbol.cpp
%define cmake_args -DCMAKE_PREFIX_PATH="%{cmake_prefix_path};${LIBIBERTY_ROOT};${FLEX_ROOT};${BISON_ROOT}" -DTBB_ROOT_DIR=${TBB_ROOT} -DROCPROFSYS_USE_BFD=ON -DROCPROFSYS_USE_PYTHON=ON -DROCPROFSYS_BUILD_PYTHON=OFF -DROCPROFSYS_BUILD_DYNINST=OFF -DROCPROFSYS_BUILD_TBB=OFF -DROCPROFSYS_BUILD_LIBUNWIND=OFF -DROCPROFSYS_BUILD_BOOST=OFF -DROCPROFSYS_BUILD_LIBIBERTY=OFF -DROCPROFSYS_BUILD_ELFUTILS=OFF -DElfUtils_ROOT_DIR=${ELFUTILS_ROOT} -DElfUtils_INCLUDEDIR=${ELFUTILS_ROOT}/include -DElfUtils_LIBRARYDIR=${ELFUTILS_ROOT}/lib -DROCPROFILER_BUILD_SQLITE3=OFF -DROCPROFSYS_BUILD_NLOHMANN_JSON=OFF -DROCPROFSYS_BUILD_EXAMPLES=OFF -DROCPROFSYS_BUILD_TESTING=OFF -DCMAKE_FIND_DEBUG_MODE=OFF -DROCPROFSYS_USE_PAPI=OFF -DPython3_ROOT_DIR=$PYTHON3_ROOT
## INCLUDE rocm-systems-build
