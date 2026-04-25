## INCLUDE rocm-config
### RPM external rocshmem %{rocm_version_num}

Source0: https://github.com/ROCm/rocSHMEM/archive/refs/tags/%{rocm_version}.tar.gz

Requires: rocm-core rocm-llvm rocr-runtime rocm-cmake hip
Requires: openmpi comgr

%prep
%setup -q -n rocSHMEM-%{rocm_version}

%build
cmake \
  -B %{_builddir}/build \
  -S %{_builddir}/rocSHMEM-%{rocm_version} \
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
