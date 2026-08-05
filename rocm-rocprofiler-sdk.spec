## INCLUDE rocm-config
### RPM external rocm-rocprofiler-sdk %{rocm_version_num}
BuildRequires: rocm-cmake cmake gmake
Requires: rocm-core rocm-llvm rocr-runtime rocprofiler rocm-comgr
Requires: fmt glog sqlite py3-pybind11 aqlprofile rocprofiler-register
Patch0: rocm-rocprofiler-sdk
%define rocm_project rocprofiler-sdk
%define ROCMPreBuild pushd %{_builddir}/rocm-systems/projects/rocprofiler-sdk; patch -p1 < %{PATCH0}; sed -i '2i\include(CPack)' CMakeLists.txt; popd; export CC=${ROCM_LLVM_ROOT}/bin/amdclang; export CXX=${ROCM_LLVM_ROOT}/bin/amdclang++
%define cmake_args -DROCPROFILER_BUILD_TESTS=OFF -DROCPROFILER_BUILD_FMT=OFF -DROCPROFILER_BUILD_GHC_FS=OFF -DROCPROFILER_BUILD_GLOG=OFF -DROCPROFILER_BUILD_PYBIND11=OFF -DROCPROFILER_BUILD_SQLITE3=OFF -DCPACK_ENABLED=OFF -DCMAKE_CXX_FLAGS="-include fstream -include array -include memory -include unistd.h -include cstdint -I$ROCM_LLVM_ROOT/lib/llvm/include -I$ROCM_LLVM_ROOT/include -I$ROCM_COMGR_ROOT/include -I$SQLITE_ROOT/include" -DCMAKE_EXE_LINKER_FLAGS="-L$SQLITE_ROOT/lib" -DCMAKE_SHARED_LINKER_FLAGS="-L$SQLITE_ROOT/lib"
%define ROCMPostPost %{relocateConfig}/lib/cmake/rocprofiler-sdk/rocprofiler-sdk-config.cmake
## INCLUDE rocm-systems-build
