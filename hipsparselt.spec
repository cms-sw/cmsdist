## INCLUDE rocm-config
### RPM external hipsparselt %{rocm_version}
Source0: https://github.com/ROCm/rocm-libraries/archive/refs/tags/%{rocm_version}.tar.gz
Requires: hipsparse msgpack-cxx rocm-core rocm-smi-lib rocminfo roctracer rocr-runtime rocm-cmake boost
Requires: py3-joblib py3-PyYAML py3-msgpack py3-packaging rocm-llvm python3 comgr

%prep
%setup -q -n rocm-libraries-%{realversion}

%build
CMAKE_ARGS=(
  -B %{_builddir}/build
  -S %{_builddir}/rocm-libraries-%{realversion}/projects/%{n}
  -DCMAKE_CXX_COMPILER=${ROCM_LLVM_ROOT}/lib/llvm/bin/clang++
  -DCMAKE_INSTALL_PREFIX=%{i}
  -DCMAKE_PREFIX_PATH="%{cmake_prefix_path}"
  -DBUILD_CLIENTS_TESTS=off
  -DGPU_TARGETS="gfx942"
  -DCMAKE_CXX_FLAGS="-I$BOOST_ROOT/include -I$ROCTRACER_ROOT/include"
  -DHIPSPARSELT_ENABLE_CLIENT=OFF
  -DHIPSPARSELT_ENABLE_FORTRAN=OFF
)

cmake "${CMAKE_ARGS[@]}"

make -C %{_builddir}/build %{makeprocesses}

%install
make -C %{_builddir}/build %{makeprocesses} install
