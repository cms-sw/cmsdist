## INCLUDE rocm-config
### RPM external hipblas %{rocm_version_num}
Source0: %{rocm_libraries_source}%{n}.tar.gz
Requires: roctracer hipblas-common python3 rocr-runtime rocblas rocsparse rocsolver

%prep
%setup -q -n %{n}

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
      -S %{_builddir}/%{n} \
      "${CMAKE_ARGS[@]}"

make -C %{_builddir}/build %{makeprocesses}

%install
make -C %{_builddir}/build %{makeprocesses} install
