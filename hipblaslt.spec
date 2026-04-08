## INCLUDE rocm-config
### RPM external hipblaslt %{rocm_version_num}
Source0: https://github.com/ROCm/rocm-libraries/archive/refs/tags/%{rocm_version}.tar.gz
Requires: hip rocm-core rocm-llvm rocr-runtime rocm-cmake hipblas-common roctracer rocm-smi-lib msgpack-cxx boost google-test amdsmi
## INCLUDE rocm-flags

%prep
%setup -q -n rocm-libraries-therock-7.12

%build
CMAKE_ARGS=(
  -B %{_builddir}/build
  -S %{_builddir}/rocm-libraries-therock-7.12/projects/%{n}
  -DCMAKE_INSTALL_PREFIX=%{i}
  -DCMAKE_C_COMPILER=$ROCM_LLVM_ROOT/bin/amdclang
  -DCMAKE_CXX_COMPILER=$ROCM_LLVM_ROOT/bin/amdclang++
  -DCMAKE_PREFIX_PATH="%{cmake_prefix_path}"
  -DBUILD_CLIENTS_TESTS=off
  -DHIPBLASLT_ENABLE_DEVICE=off
  -DHIPBLASLT_ENABLE_CLIENT=off
  -DTENSILELITE_BUILD_TESTING=off
  -DORIGAMI_BUILD_TESTING=off
  -DGPU_TARGETS="gfx908;gfx90a;gfx942;gfx1100;gfx1102"
  -DCMAKE_CXX_FLAGS="-I$ROCTRACER_ROOT/include"
)

cmake "${CMAKE_ARGS[@]}"

make -C %{_builddir}/build %{makeprocesses}

%install
make -C %{_builddir}/build %{makeprocesses} install
