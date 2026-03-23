### RPM external rocm-offload 7.10

Source0: https://github.com/ROCm/llvm-project/archive/refs/tags/therock-7.10.tar.gz

Requires: rocm-core python3 cmake rocm-llvm hsa-rocr

%prep
%setup -q -n llvm-project-therock-%{realversion}

%build
mkdir -p %{_builddir}/build
cd %{_builddir}/build

cmake \
  -S %{_builddir}/llvm-project-therock-%{realversion}/offload \
  -DCMAKE_INSTALL_PREFIX=%{i} \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_PREFIX_PATH="%{cmake_prefix_path}" \
  -DCMAKE_C_COMPILER=${ROCM_LLVM_ROOT}/bin/clang \
  -DCMAKE_CXX_COMPILER=${ROCM_LLVM_ROOT}/bin/clang++ \
  -DBUILD_TESTING=OFF

make %{makeprocesses}

%install
make -C %{_builddir}/build %{makeprocesses} install
