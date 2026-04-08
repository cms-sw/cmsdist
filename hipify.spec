## INCLUDE rocm-config 
### RPM external hipify 7.2.1
Source0: https://github.com/ROCm/HIPIFY/archive/refs/tags/rocm-7.2.1.tar.gz
Requires: rocm-llvm

%prep
%setup -q -n HIPIFY-rocm-%{realversion}

%build
CMAKE_ARGS=(
  -B %{_builddir}/build
  -S %{_builddir}/HIPIFY-rocm-%{realversion}
  -DCMAKE_INSTALL_PREFIX=%{i}
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_C_COMPILER=${ROCM_LLVM_ROOT}/bin/clang \
  -DCMAKE_CXX_COMPILER=${ROCM_LLVM_ROOT}/bin/clang++ \
  -DLLVM_DIR=${ROCM_LLVM_ROOT}/lib/cmake/llvm \
  -DCMAKE_PREFIX_PATH="%{cmake_prefix_path}"
)

cmake "${CMAKE_ARGS[@]}"

make -C %{_builddir}/build %{makeprocesses}
%install
make -C %{_builddir}/build %{makeprocesses} install
