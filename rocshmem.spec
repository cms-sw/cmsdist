## INCLUDE rocm-config
### RPM external rocshmem %{rocm_version_num}

Source0: %{rocm_systems_source}%{n}.tar.gz

Requires: rocm-core rocm-llvm rocr-runtime rocm-cmake hip
Requires: openmpi

%prep
%setup -q -n %{n}

%build

cmake \
  -B %{_builddir}/build \
  -S %{_builddir}/%{n} \
  -DCMAKE_C_COMPILER=${ROCM_LLVM_ROOT}/bin/amdclang \
  -DCMAKE_CXX_COMPILER=${ROCM_LLVM_ROOT}/bin/amdclang++ \
  -DCMAKE_INSTALL_PREFIX=%{i} \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_PREFIX_PATH="%{cmake_prefix_path}" \
  -DROCM_PATH=$ROCM_LLVM_ROOT \
  -DUSE_EXTERNAL_MPI=ON \
  -DBUILD_TESTING=OFF \
  -DCMAKE_CXX_FLAGS="-I$ROCM_CORE_ROOT/include"

make -C %{_builddir}/build %{makeprocesses} VERBOSE=1

%install
make -C %{_builddir}/build %{makeprocesses} install
