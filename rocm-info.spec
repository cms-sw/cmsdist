## INCLUDE rocm-sources
### RPM external rocm-info %{rocm_version}

Source0: %{rocm_systems_source}
BuildRequires: rocm-llvm rocm-cmake rocm-core hsa-rocr
Requires: rocm-llvm rocm-core hsa-rocr
%prep
%setup -q -n rocm-systems-rocm-%{realversion}
%build
cmake -B %{_builddir}/build-rocm-info -S %{_builddir}/rocm-systems-rocm-%{realversion}/projects/rocminfo \
  -DCMAKE_INSTALL_PREFIX=%{i} \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_PREFIX_PATH="%{cmake_prefix_path}" \
  -DCMAKE_C_COMPILER=${ROCM_LLVM_ROOT}/bin/amdclang \
  -DCMAKE_CXX_COMPILER=${ROCM_LLVM_ROOT}/bin/amdclang++ \
  -DROCM_DIR=${ROCM_LLVM_ROOT}
make -C %{_builddir}/build-rocm-info %{makeprocesses}
%install
make -C %{_builddir}/build-rocm-info %{makeprocesses} install
