### RPM external hsa-rocr 7.10
## INCLUDE cpp-standard
Source0: https://github.com/ROCm/rocm-systems/releases/download/therock-7.10/rocr-runtime.tar.gz
BuildRequires: rocm-llvm rocm-cmake rocm-core numactl
Requires: rocm-llvm rocm-core zlib libxml2 rocprofiler-register numactl
%prep
%setup -q -n rocr-runtime
%build
mkdir -p %{_builddir}/build-hsa-rocr
cd %{_builddir}/build-hsa-rocr
export PKG_CONFIG_PATH=/usr/lib64/pkgconfig
cmake \
  -S %{_builddir}/rocr-runtime \
  -DCMAKE_INSTALL_PREFIX=%{i} \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_PREFIX_PATH="%{cmake_prefix_path}" \
  -DCMAKE_C_COMPILER=${ROCM_LLVM_ROOT}/bin/clang \
  -DCMAKE_CXX_COMPILER=${ROCM_LLVM_ROOT}/bin/clang++ \
  -DCMAKE_C_FLAGS="-I${NUMACTL_ROOT}/include" \
  -DCMAKE_CXX_FLAGS="-I${NUMACTL_ROOT}/include" \
  -DLLVM_DIR=${ROCM_LLVM_ROOT}/lib/cmake/llvm \
  -DBUILD_SHARED_LIBS=ON \
  -DSO_VERSION_STRING=1.18.0
make %{makeprocesses}
%install
make -C %{_builddir}/build-hsa-rocr %{makeprocesses} install
