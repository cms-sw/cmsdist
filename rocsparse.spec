## INCLUDE rocm-config
### RPM external rocsparse %{rocm_version_num}
## INCLUDE rocm-config
Requires: rocprim rocblas
%define ROCMPreBuild export HIP_DEVICE_LIB_PATH=$ROCM_LLVM_ROOT/amdgcn/bitcode
## INCLUDE rocm-libraries-build
