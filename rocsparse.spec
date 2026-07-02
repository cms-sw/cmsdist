## INCLUDE rocm-config
### RPM external rocsparse %{rocm_version_num}
## INCLUDE rocm-config
Source0: https://github.com/ROCm/rocSPARSE/archive/refs/tags/rocm-%{rocm_version_num}.tar.gz
BuildRequires: rocm-cmake
Requires: hip rocm-core rocm-llvm rocr-runtime comgr rocprim rocblas

%prep
%setup -q -n rocSPARSE-%{rocm_version}

%build
export HIP_DEVICE_LIB_PATH=$ROCM_LLVM_ROOT/amdgcn/bitcode
CMAKE_ARGS=(
  -B %{_builddir}/build
  -S %{_builddir}/rocSPARSE-%{rocm_version}
  -DCMAKE_INSTALL_PREFIX=%{i}
  -DCMAKE_C_COMPILER=$ROCM_LLVM_ROOT/bin/amdclang
  -DCMAKE_CXX_COMPILER=$ROCM_LLVM_ROOT/bin/amdclang++
  -DCMAKE_PREFIX_PATH="%{cmake_prefix_path}"
  -DBUILD_CLIENTS_TESTS=off
  -DHIP_ROOT=$HIP_ROOT
  -DGPU_TARGETS="%{rocm_targets}"
  $LIB_ARGS
)

cmake "${CMAKE_ARGS[@]}"

make -C %{_builddir}/build %{makeprocesses}

%install
make -C %{_builddir}/build %{makeprocesses} install
