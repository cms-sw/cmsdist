## INCLUDE rocm-sources
### RPM external rocm-smi-lib %{rocm_version}

Source0: %{rocm_systems_source}

Requires: rocm-core rocm-llvm hsa-rocr cmake rocm-cmake hip

%prep
%setup -q -n rocm-systems-rocm-%{rocm_version}

%build
mkdir -p %{_builddir}/build
cd %{_builddir}/build

cmake \
  -S %{_builddir}/rocm-systems-rocm-%{realversion}/projects/rocm-smi-lib \
  -DCMAKE_INSTALL_PREFIX=%{i} \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_PREFIX_PATH="%{cmake_prefix_path}" \
  -DCMAKE_C_COMPILER=${ROCM_LLVM_ROOT}/bin/amdclang \
  -DCMAKE_CXX_COMPILER=${ROCM_LLVM_ROOT}/bin/amdclang++ \
  -DBUILD_TESTING=OFF

make %{makeprocesses} VERBOSE=1

%install
make -C %{_builddir}/build %{makeprocesses} install
