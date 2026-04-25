## INCLUDE rocm-config
### RPM external rocm-rocprofiler-sdk %{rocm_version_num}

Source0: https://github.com/ROCm/rocprofiler-sdk/archive/refs/tags/rocm-%{realversion}.tar.gz
Requires: rocm-core rocm-llvm rocr-runtime rocm-cmake rocprofiler comgr
Requires: fmt glog sqlite py3-pybind11 aqlprofile rocprofiler-register
Patch0: rocm-rocprofiler-sdk
Patch1: rocm-rocprofiler-sdk-externals

%prep
%setup -q -n rocprofiler-sdk-rocm-%{realversion}

%patch0 -p1 
%patch1 -p1 

%build
sed -i '2i\include(CPack)' %{_builddir}/rocprofiler-sdk-rocm-%{realversion}/CMakeLists.txt

export CC=${ROCM_LLVM_ROOT}/bin/amdclang
export CXX=${ROCM_LLVM_ROOT}/bin/amdclang++

cmake \
  -B %{_builddir}/build \
  -S %{_builddir}/rocprofiler-sdk-rocm-%{realversion} \
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
  -DCMAKE_CXX_FLAGS="-include fstream -include array -include memory -include unistd.h -I$ROCM_LLVM_ROOT/lib/llvm/include -I$ROCM_LLVM_ROOT/include -I$COMGR_ROOT/include"

make -C %{_builddir}/build %{makeprocesses} VERBOSE=1

%install
make -C %{_builddir}/build %{makeprocesses} install
