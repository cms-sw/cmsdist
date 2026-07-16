## INCLUDE rocm-config
### RPM external rocr-runtime %{rocm_version_num}
Source: %{rocm_systems_source}
Requires: rocm-core zlib libxml2 rocprofiler-register numactl rocm-llvm

%prep
%setup -q -n rocm-systems/projects/%{n}

%build
export ROCM_PATH=$ROCM_LLVM_ROOT
export ROCM_DEVICE_LIB_PATH=$ROCM_LLVM_ROOT/amdgcn/bitcode

cmake \
  -S %{_builddir}/rocm-systems/projects/%{n} \
  -B %{_builddir}/build \
  -DCMAKE_CXX_COMPILER=$ROCM_LLVM_ROOT/lib/llvm/bin/clang++ \
  -DCMAKE_BUILD_TYPE=%{cmake_build_type} \
  -DCMAKE_INSTALL_PREFIX=%{i} \
  -DCMAKE_PREFIX_PATH="%{cmake_prefix_path}" \
  -DBUILD_SHARED_LIBS=ON \
  -DCMAKE_C_FLAGS="-I${NUMACTL_ROOT}/include" \
  -DCMAKE_CXX_FLAGS="-I${NUMACTL_ROOT}/include --rocm-path=$ROCM_LLVM_ROOT"

make -C %{_builddir}/build %{makeprocesses} VERBOSE=1
%install
make -C %{_builddir}/build %{makeprocesses} install  VERBOSE=1
%post
%{relocateConfig}/lib64/cmake/hsakmt/hsakmtTargets.cmake
