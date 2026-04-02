### RPM external rocm-rccl 7.11
## NOCOMPILER
Source0: https://github.com/ROCm/rocm-systems/releases/download/therock-7.11/rccl.tar.gz

Requires: rocm-core rocm-llvm hip hsa-rocr rocm-amd-smi-lib hipify rocm-info rocprofiler-register rocm-smi-lib
Requires: python3

%prep
%setup -q -n rccl

%build
mkdir -p %{_builddir}/build
cd %{_builddir}/build

export ROCM_PATH=${ROCM_LLVM_ROOT}
export CC=${ROCM_LLVM_ROOT}/bin/amdclang
export CXX=${ROCM_LLVM_ROOT}/bin/amdclang++

grep -q 'math(EXPR num_linker_jobs "(${memory_in_gb} + 15) / 16")' %{_builddir}/rccl/CMakeLists.txt
#sed -i 's/math(EXPR num_linker_jobs "(${memory_in_gb} + 15) \/ 16")/math(EXPR num_linker_jobs "${memory_in_gb} \/ 6*2")/' %{_builddir}/rccl/CMakeLists.txt

echo "%{cmake_prefix_path}"

cmake \
  -S %{_builddir}/rccl \
  -DCMAKE_INSTALL_PREFIX=%{i} \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_PREFIX_PATH="%{cmake_prefix_path}" \
  -DBUILD_TESTS=OFF \
  -DROCM_PATH=${HIP_ROOT} \
  -DEXPLICIT_ROCM_VERSION=7.1.0 \
  -DROCM_CORE_PATH=${ROCM_CORE_PATH} \
  -DGPU_TARGETS="gfx908:sramecc+;gfx90a:sramecc+;gfx942:sramecc+;gfx1030;gfx1100;gfx1102" \
  -DCMAKE_CXX_FLAGS="--rocm-device-lib-path=${ROCM_LLVM_ROOT}/amdgcn/bitcode -I${ROCM_CORE_ROOT}/include -include __clang_hip_runtime_wrapper.h" \
  -DCMAKE_EXE_LINKER_FLAGS="-L${HIP_ROOT}/lib" \
  -DCMAKE_SHARED_LINKER_FLAGS="-L${HIP_ROOT}/lib"

make %{makeprocesses} VERBOSE=1

%install
make -C %{_builddir}/build %{makeprocesses} install
