### RPM external rocm-roctracer 7.10

Source0: https://github.com/ROCm/rocm-systems/releases/download/therock-7.10/roctracer.tar.gz
Requires: rocm-core rocm-llvm hsa-rocr python3 cmake hip rocm-info

%prep
%setup -q -n roctracer

%build
mkdir -p %{_builddir}/build
cd %{_builddir}/build

sed -i 's/add_subdirectory(test)/# add_subdirectory(test)/' %{_builddir}/roctracer/CMakeLists.txt

cmake \
  -S %{_builddir}/roctracer \
  -DCMAKE_INSTALL_PREFIX=%{i} \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_PREFIX_PATH="%{cmake_prefix_path}" \
  -DCMAKE_C_COMPILER=${ROCM_LLVM_ROOT}/bin/clang \
  -DCMAKE_CXX_COMPILER=${ROCM_LLVM_ROOT}/bin/clang++ \
  -DBUILD_TESTS=OFF \
  -DROCM_PATH=${HIP_ROOT}

make %{makeprocesses}

%install
make -C %{_builddir}/build %{makeprocesses} install
