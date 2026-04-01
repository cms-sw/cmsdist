## INCLUDE rocm-sources
### RPM external hipblas %{rocm_version}
Source0: https://github.com/ROCm/rocm-libraries/archive/refs/tags/rocm-%{rocm_version}.tar.gz
Requires: rocm-roctracer hipblas-common python3 hsa-rocr rocblas rocsparse

%prep
%setup -q -n rocm-libraries-rocm-%{realversion}

%build
CMAKE_ARGS=(
  -DCMAKE_INSTALL_PREFIX=%{i}
  -DCMAKE_C_COMPILER=$ROCM_LLVM_ROOT/bin/amdclang
  -DCMAKE_CXX_COMPILER=$ROCM_LLVM_ROOT/bin/amdclang++
  -DCMAKE_PREFIX_PATH="%{cmake_prefix_path}"
  -DBUILD_CLIENTS_TESTS=off
  -DGPU_TARGETS="gfx908;gfx90a;gfx942;gfx1030;gfx1100;gfx1102"
  -DCMAKE_CXX_FLAGS="-I$BOOST_ROOT/include"
)

cmake -B %{_builddir}/build \
      -S %{_builddir}/rocm-libraries-rocm-%{realversion}/projects/%{n} \
      "${CMAKE_ARGS[@]}"

make -C %{_builddir}/build %{makeprocesses}

%install
make -C %{_builddir}/build %{makeprocesses} install
