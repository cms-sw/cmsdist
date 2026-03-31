## INCLUDE rocm-sources
### RPM external rocm-roctracer %{rocm_version}

Source0: %{rocm_systems_source}
Requires: rocm-core rocm-llvm hsa-rocr python3 cmake hip rocm-info

%prep
%setup -q -n rocm-systems-rocm-%{realversion}

%build
mkdir -p %{_builddir}/build
cd %{_builddir}/build

sed -i 's/add_subdirectory(test)/# add_subdirectory(test)/' %{_builddir}/rocm-systems-rocm-%{realversion}/projects/roctracer/CMakeLists.txt

cmake \
  -S %{_builddir}/rocm-systems-rocm-%{realversion}/projects/roctracer \
  -DCMAKE_INSTALL_PREFIX=%{i} \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_PREFIX_PATH="%{cmake_prefix_path}" \
  -DCMAKE_C_COMPILER=${ROCM_LLVM_ROOT}/bin/amdclang \
  -DCMAKE_CXX_COMPILER=${ROCM_LLVM_ROOT}/bin/amdclang++ \
  -DBUILD_TESTS=OFF \
  -DROCM_PATH=${HIP_ROOT}

make %{makeprocesses}

%install
make -C %{_builddir}/build %{makeprocesses} install
