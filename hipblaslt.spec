## INCLUDE rocm-sources
### RPM external hipblaslt %{rocm_version}
Source0: https://github.com/ROCm/rocm-libraries/archive/refs/tags/rocm-%{rocm_version}.tar.gz
Requires: hip rocm-core rocm-llvm hsa-rocr rocm-cmake hipblas-common rocm-roctracer rocm-smi-lib msgpack-cxx boost google-test
## INCLUDE rocm-flags

%prep
%setup -q -n rocm-libraries-rocm-%{realversion}

%build
CMAKE_ARGS=(
  -B %{_builddir}/build
  -S %{_builddir}/rocm-libraries-rocm-%{realversion}/projects/%{n}
  -DCMAKE_INSTALL_PREFIX=%{i}
  -DCMAKE_C_COMPILER=$ROCM_LLVM_ROOT/bin/amdclang
  -DCMAKE_CXX_COMPILER=$ROCM_LLVM_ROOT/bin/amdclang++
  -DCMAKE_PREFIX_PATH="%{cmake_prefix_path}"
  -DBUILD_CLIENTS_TESTS=off
  -DHIPBLASLT_ENABLE_DEVICE=off
  -DHIPBLASLT_ENABLE_CLIENT=off
  -DTENSILELITE_BUILD_TESTING=off
  -DORIGAMI_BUILD_TESTING=off
  -DGPU_TARGETS="gfx908;gfx90a;gfx942;gfx1100"
  -DCMAKE_CXX_FLAGS="-I$ROCM_ROCTRACER_ROOT/include"
)

cmake "${CMAKE_ARGS[@]}"

make -C %{_builddir}/build %{makeprocesses}

%install
make -C %{_builddir}/build %{makeprocesses} install
