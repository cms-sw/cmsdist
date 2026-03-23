### RPM external rocm-aqlprofile 7.10
Source: https://github.com/ROCm/rocm-systems/releases/download/therock-7.10/aqlprofile.tar.gz
Requires: rocm-core rocm-llvm hsa-rocr python3 cmake

%prep
%setup -q -n aqlprofile

%build
mkdir -p %{_builddir}/build
cd %{_builddir}/build

cmake \
  -S %{_builddir}/aqlprofile \
  -DCMAKE_INSTALL_PREFIX=%{i} \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_PREFIX_PATH="%{cmake_prefix_path}" \
  -DCMAKE_C_COMPILER=${ROCM_LLVM_ROOT}/bin/clang \
  -DCMAKE_CXX_COMPILER=${ROCM_LLVM_ROOT}/bin/clang++ \
  -DBUILD_TESTING=OFF

make %{makeprocesses}

%install
make -C %{_builddir}/build %{makeprocesses} install
