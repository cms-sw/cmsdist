### RPM external rocm-smi-lib 7.10

Source0: https://github.com/ROCm/rocm-systems/releases/download/therock-7.10/rocm-smi-lib.tar.gz

Requires: rocm-core rocm-llvm hsa-rocr cmake rocm-cmake hip

%prep
%setup -q -n rocm-smi-lib

%build
mkdir -p %{_builddir}/build
cd %{_builddir}/build

cmake \
  -S %{_builddir}/rocm-smi-lib \
  -DCMAKE_INSTALL_PREFIX=%{i} \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_PREFIX_PATH="%{cmake_prefix_path}" \
  -DCMAKE_C_COMPILER=${ROCM_LLVM_ROOT}/bin/clang \
  -DCMAKE_CXX_COMPILER=${ROCM_LLVM_ROOT}/bin/clang++ \
  -DBUILD_TESTING=OFF

make %{makeprocesses} VERBOSE=1

%install
make -C %{_builddir}/build %{makeprocesses} install
