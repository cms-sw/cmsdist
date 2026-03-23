### RPM external rocm-rccl 7.11
## NOCOMPILER
Source0: https://github.com/ROCm/rocm-systems/releases/download/therock-7.11/rccl.tar.gz

Requires: rocm-core rocm-llvm hip hsa-rocr amdsmi-rocm hipify rocm-info rocprofiler-register rocm-smi-lib
Requires: python3

%prep
%setup -q -n rccl

%build
mkdir -p %{_builddir}/build
cd %{_builddir}/build

export ROCM_PATH=${ROCM_LLVM_ROOT}
export CC=${ROCM_LLVM_ROOT}/bin/amdclang
export CXX=${ROCM_LLVM_ROOT}/bin/amdclang++

sed -i 's/math(EXPR num_linker_jobs "(${memory_in_gb} + 15) \/ 16")/set(num_linker_jobs 8)/' %{_builddir}/rccl/CMakeLists.txt

cmake \
  -S %{_builddir}/rccl \
  -DCMAKE_INSTALL_PREFIX=%{i} \
  -DCMAKE_BUILD_TYPE=Release \
  "-DCMAKE_PREFIX_PATH=${HIP_ROOT};${HSA_ROCR_ROOT};${ROCPROFILER_REGISTER_ROOT};${ROCM_SMI_LIB_ROOT};${ROCM_CORE_ROOT};${ROCM_LLVM_ROOT}" \
  -DBUILD_TESTS=OFF \
  -DROCM_PATH=${HIP_ROOT} \
  -DEXPLICIT_ROCM_VERSION=7.1.0 \
  -DROCM_CORE_PATH=${ROCM_CORE_PATH} \
  -DGPU_TARGETS="gfx940;gfx1030" \
  -DCMAKE_CXX_FLAGS="--rocm-device-lib-path=${ROCM_LLVM_ROOT}/amdgcn/bitcode -I${ROCM_CORE_ROOT}/include -include __clang_hip_runtime_wrapper.h"

make %{makeprocesses} VERBOSE=1

%install
make -C %{_builddir}/build %{makeprocesses} install
