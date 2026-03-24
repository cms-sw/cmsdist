### RPM external rocm-rocprofiler-sdk 7.10

Source0: https://github.com/ROCm/rocm-systems/releases/download/therock-7.10/rocprofiler-sdk.tar.gz
Requires: rocm-core rocm-llvm hsa-rocr rocm-cmake rocm-rocprofiler
Requires: fmt glog sqlite py3-pybind11 rocm-aqlprofile rocprofiler-register
Patch0: rocm-rocprofiler-sdk
Patch1: rocm-rocprofiler-sdk-externals

%prep
%setup -q -n rocprofiler-sdk

%patch0 -p1 
%patch1 -p1 

%build
sed -i '2i\include(CPack)' %{_builddir}/rocprofiler-sdk/CMakeLists.txt
mkdir -p %{_builddir}/build
cd %{_builddir}/build

export CC=${ROCM_LLVM_ROOT}/bin/amdclang
export CXX=${ROCM_LLVM_ROOT}/bin/amdclang++

cmake \
  -S %{_builddir}/rocprofiler-sdk \
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
  -DCMAKE_CXX_FLAGS="-include fstream -include array -include memory"
  

make %{makeprocesses} VERBOSE=1

%install
make -C %{_builddir}/build %{makeprocesses} install
