### RPM external rocm-info 7.10
## INCLUDE cpp-standard
Source0: https://github.com/ROCm/rocm-systems/releases/download/therock-7.10/rocminfo.tar.gz
BuildRequires: rocm-llvm rocm-cmake rocm-core hsa-rocr
Requires: rocm-llvm rocm-core hsa-rocr
%prep
%setup -q -n rocminfo
%build
cmake -B %{_builddir}/build-rocm-info -S %{_builddir}/rocminfo \
  -DCMAKE_INSTALL_PREFIX=%{i} \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_PREFIX_PATH="%{cmake_prefix_path}" \
  -DCMAKE_C_COMPILER=${ROCM_LLVM_ROOT}/bin/clang \
  -DCMAKE_CXX_COMPILER=${ROCM_LLVM_ROOT}/bin/clang++ \
  -DROCM_DIR=${ROCM_LLVM_ROOT}
make -C %{_builddir}/build-rocm-info %{makeprocesses}
%install
make -C %{_builddir}/build-rocm-info %{makeprocesses} install
