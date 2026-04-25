## INCLUDE rocm-config
### RPM external rocblas %{rocm_version_num}
Source0: https://github.com/ROCm/rocm-libraries/archive/refs/tags/%{rocm_version}.tar.gz
Requires: roctracer hipblaslt hipblas-common python3 rocr-runtime msgpack-cxx boost rocminfo rocm-llvm comgr

%prep
%setup -q -n rocm-libraries-%{rocm_version}

%build
export ROCM_PATH=$ROCM_LLVM_ROOT

CMAKE_ARGS=(
  -B %{_builddir}/build
  -S %{_builddir}/rocm-libraries-%{rocm_version}/projects/%{n}
  -DCMAKE_INSTALL_PREFIX=%{i}
  -DCMAKE_C_COMPILER=$ROCM_LLVM_ROOT/bin/amdclang
  -DCMAKE_CXX_COMPILER=$ROCM_LLVM_ROOT/bin/amdclang++
  -DCMAKE_PREFIX_PATH="%{cmake_prefix_path}"
  -DBUILD_CLIENTS_TESTS=off
  -DGPU_TARGETS="gfx908:xnack-;gfx90a;gfx942;gfx1030;gfx1100;gfx1102"
  -DCMAKE_CXX_FLAGS="-I$BOOST_ROOT/include --rocm-path=$ROCM_LLVM_ROOT/amdgcn/bitcode"
)
cmake "${CMAKE_ARGS[@]}"

%install
make -C %{_builddir}/build %{makeprocesses} install
