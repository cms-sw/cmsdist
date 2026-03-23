### RPM external rocm-dbgapi 7.1.0

Source: https://github.com/ROCm/ROCdbgapi/archive/refs/tags/rocm-7.1.0.tar.gz
Requires: hsa-rocr rocm-core rocm-llvm python3 cmake

%prep
%setup -q -n ROCdbgapi-rocm-%{realversion}

%build
mkdir -p %{_builddir}/build
cd %{_builddir}/build

cmake \
  -S %{_builddir}/ROCdbgapi-rocm-%{realversion} \
  -DCMAKE_INSTALL_PREFIX=%{i} \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_PREFIX_PATH="%{cmake_prefix_path}" \
  -DCMAKE_C_COMPILER=${ROCM_LLVM_ROOT}/bin/clang \
  -DCMAKE_CXX_COMPILER=${ROCM_LLVM_ROOT}/bin/clang++ \
  -DBUILD_TESTING=OFF

make %{makeprocesses}

%install
make -C %{_builddir}/build %{makeprocesses} install
