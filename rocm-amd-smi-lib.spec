## INCLUDE rocm-sources
### RPM external rocm-amd-smi-lib %{rocm_version}

Source0: https://github.com/ROCm/amdsmi/archive/refs/tags/rocm-%{rocm_version}.tar.gz
Requires: rocm-core python3 rocm-llvm

%prep
%setup -q -n amdsmi-rocm-%{realversion}

%build
mkdir -p %{_builddir}/build
cd %{_builddir}/build

cmake \
  -S %{_builddir}/amdsmi-rocm-%{realversion} \
  -DCMAKE_INSTALL_PREFIX=%{i} \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_PREFIX_PATH="%{cmake_prefix_path}" \
  -DCMAKE_C_COMPILER=${ROCM_LLVM_ROOT}/bin/amdclang \
  -DCMAKE_CXX_COMPILER=${ROCM_LLVM_ROOT}/bin/amdclang++ \
  -DBUILD_TESTING=OFF

make %{makeprocesses}
%install
make -C %{_builddir}/build %{makeprocesses} install
