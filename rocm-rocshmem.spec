### RPM external rocm-rocshmem 7.1.0

Source0: https://github.com/ROCm/rocSHMEM/archive/refs/tags/rocm-7.1.0.tar.gz

Requires: rocm-core rocm-llvm hsa-rocr rocm-cmake hip
Requires: openmpi

%prep
%setup -q -n rocSHMEM-rocm-%{realversion}

%build
mkdir -p %{_builddir}/build
cd %{_builddir}/build

cmake \
  -B %{_builddir}/build \
  -S %{_builddir}/rocSHMEM-rocm-%{realversion} \
  -DCMAKE_C_COMPILER=${ROCM_LLVM_ROOT}/bin/amdclang \
  -DCMAKE_CXX_COMPILER=${ROCM_LLVM_ROOT}/bin/amdclang++ \
  -DCMAKE_INSTALL_PREFIX=%{i} \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_PREFIX_PATH="%{cmake_prefix_path}" \
  -DROCM_PATH=$ROCM_LLVM_ROOT \
  -DUSE_EXTERNAL_MPI=ON \
  -DBUILD_TESTING=OFF

make %{makeprocesses} VERBOSE=1

%install
make -C %{_builddir}/build %{makeprocesses} install
