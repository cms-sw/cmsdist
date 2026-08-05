## INCLUDE rocm-config
### RPM external rccl %{rocm_version_num}
Requires: rocm-core rocm-llvm rocr-runtime amdsmi rocm-hip rocminfo rocprofiler-register rocm-smi-lib roctracer hipify rocm-comgr
Requires: python3
%define ROCMPreBuild export ROCM_PATH=${ROCM_LLVM_ROOT}; export CC=${ROCM_LLVM_ROOT}/bin/amdclang; export CXX=${ROCM_LLVM_ROOT}/bin/amdclang++
%define cmake_args -DBUILD_TESTS=OFF -DROCM_PATH=${ROCM_HIP_ROOT}  -DROCM_CORE_PATH=${ROCM_CORE_ROOT} -DEXPLICIT_ROCM_VERSION="%{realversion}.0" -DGPU_TARGETS="%{rocm_targets}" -DCMAKE_CXX_FLAGS="--rocm-device-lib-path=${ROCM_LLVM_ROOT}/amdgcn/bitcode -I${ROCM_CORE_ROOT}/include -include __clang_hip_runtime_wrapper.h -I${ROCTRACER_ROOT}/include" -DCMAKE_EXE_LINKER_FLAGS="-L${ROCM_HIP_ROOT}/lib -L${ROCTRACER_ROOT}/lib64 -L${ROCM_CORE_ROOT}/lib64" -DCMAKE_SHARED_LINKER_FLAGS="-L${ROCM_HIP_ROOT}/lib -L${ROCTRACER_ROOT}/lib64 -L${ROCM_CORE_ROOT}/lib64" -DROCM_VERSION=71300
## INCLUDE rocm-systems-build
