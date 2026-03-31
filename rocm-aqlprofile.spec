## INCLUDE rocm-sources
### RPM external rocm-aqlprofile %{rocm_version}

Source0: %{rocm_systems_source}
Requires: rocm-core rocm-llvm hsa-rocr python3 cmake
%prep
%setup -q -n rocm-systems-rocm-%{realversion}

%build
mkdir -p %{_builddir}/build
cd %{_builddir}/build

cmake \
  -S %{_builddir}/rocm-systems-rocm-%{realversion}/projects/aqlprofile \
  -DCMAKE_INSTALL_PREFIX=%{i} \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_PREFIX_PATH="%{cmake_prefix_path}" \
  -DCMAKE_C_COMPILER=${ROCM_LLVM_ROOT}/bin/amdclang \
  -DCMAKE_CXX_COMPILER=${ROCM_LLVM_ROOT}/bin/amdclang++ \
  -DBUILD_TESTING=OFF

make %{makeprocesses}

%install
make -C %{_builddir}/build %{makeprocesses} install
