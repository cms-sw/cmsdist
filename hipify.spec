## INCLUDE rocm-config
### RPM external hipify %{rocm_version_num}
Source0: git+https://github.com/ROCm/HIPIFY.git?obj=amd-develop/therock-%{rocm_version_num}&export=hipify&export=%{n}&submodules=1&output=/%{n}.tar.gz
Requires: rocm-llvm

%prep
%setup -q -n %{n}

%build
CMAKE_ARGS=(
  -B %{_builddir}/build
  -S %{_builddir}/%{n}
  -DCMAKE_INSTALL_PREFIX=%{i}
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_C_COMPILER=${ROCM_LLVM_ROOT}/lib/llvm/bin/clang \
  -DCMAKE_CXX_COMPILER=${ROCM_LLVM_ROOT}/lib/llvm/bin/clang++ \
  -DLLVM_DIR=${ROCM_LLVM_ROOT}/lib/cmake/llvm \
  -DCMAKE_PREFIX_PATH="%{cmake_prefix_path}"
)

cmake "${CMAKE_ARGS[@]}"

make -C %{_builddir}/build %{makeprocesses}
%install
make -C %{_builddir}/build %{makeprocesses} install
