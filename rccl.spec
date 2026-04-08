## INCLUDE rocm-config
### RPM external rccl %{rocm_version_num}
Source0: %{rocm_systems_source}%{n}.tar.gz

Requires: rocm-core rocm-llvm rocr-runtime amdsmi hip rocminfo rocprofiler-register rocm-smi-lib roctracer hipify
Requires: python3

%prep
%setup -q -n rccl

%build
grep -q 'math(EXPR num_linker_jobs "(${memory_in_gb} + 15) / 16")' %{_builddir}/rccl/CMakeLists.txt
#sed -i 's/math(EXPR num_linker_jobs "(${memory_in_gb} + 15) \/ 16")/math(EXPR num_linker_jobs "${memory_in_gb} \/ 6*2")/' %{_builddir}/rccl/CMakeLists.txt
export ROCM_PATH=${ROCM_LLVM_ROOT}
export CC=${ROCM_LLVM_ROOT}/bin/amdclang
export CXX=${ROCM_LLVM_ROOT}/bin/amdclang++
cmake \
  -S %{_builddir}/%{n} \
  -B %{_builddir}/build \
  -DCMAKE_INSTALL_PREFIX=%{i} \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_PREFIX_PATH="%{cmake_prefix_path}" \
  -DBUILD_TESTS=OFF \
  -DROCM_PATH=${HIP_ROOT} \
  -DROCM_CORE_PATH=${ROCM_CORE_PATH} \
  -DEXPLICIT_ROCM_VERSION="7.2.1" \
  -DGPU_TARGETS="gfx908:sramecc+;gfx90a:sramecc+;gfx942:sramecc+;gfx1030;gfx1100;gfx1102" \
  -DCMAKE_CXX_FLAGS="--rocm-device-lib-path=${ROCM_LLVM_ROOT}/amdgcn/bitcode -I${ROCM_CORE_ROOT}/include -include __clang_hip_runtime_wrapper.h" \
  -DCMAKE_EXE_LINKER_FLAGS="-L${HIP_ROOT}/lib" \
  -DCMAKE_SHARED_LINKER_FLAGS="-L${HIP_ROOT}/lib"

make -C %{_builddir}/build %{makeprocesses} VERBOSE=1

%install
make -C %{_builddir}/build %{makeprocesses} install
