## INCLUDE rocm-config
### RPM external rocm-rocprofiler-sdk %{rocm_version_num}

Source0: %{rocm_systems_source}
BuildRequires: rocm-cmake
Requires: rocm-core rocm-llvm rocr-runtime rocprofiler rocm-comgr
Requires: fmt glog sqlite py3-pybind11 aqlprofile rocprofiler-register
Patch0: rocm-rocprofiler-sdk
BuildRequires: cmake gmake

%prep
%setup -q -n rocm-systems

%build
pushd %{_builddir}/rocm-systems/projects/rocprofiler-sdk
patch -p1 < %{PATCH0}
sed -i '2i\include(CPack)' CMakeLists.txt
popd

export CC=${ROCM_LLVM_ROOT}/bin/amdclang
export CXX=${ROCM_LLVM_ROOT}/bin/amdclang++

cmake \
  -B %{_builddir}/build \
  -S %{_builddir}/rocm-systems/projects/rocprofiler-sdk \
  -DCMAKE_INSTALL_PREFIX=%{i} \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_PREFIX_PATH="%{cmake_prefix_path}" \
  -DROCPROFILER_BUILD_TESTS=OFF \
  -DROCPROFILER_BUILD_FMT=OFF \
  -DROCPROFILER_BUILD_GHC_FS=OFF \
  -DROCPROFILER_BUILD_GLOG=OFF \
  -DROCPROFILER_BUILD_PYBIND11=OFF \
  -DROCPROFILER_BUILD_SQLITE3=OFF \
  -DCPACK_ENABLED=OFF \
  -DCMAKE_CXX_FLAGS="-include fstream -include array -include memory -include unistd.h -include cstdint -I$ROCM_LLVM_ROOT/lib/llvm/include -I$ROCM_LLVM_ROOT/include -I$ROCM_COMGR_ROOT/include"

make -C %{_builddir}/build %{makeprocesses} VERBOSE=1

%install
make -C %{_builddir}/build %{makeprocesses} install

%post
%{relocateConfig}/lib/cmake/rocprofiler-sdk/rocprofiler-sdk-config.cmake
