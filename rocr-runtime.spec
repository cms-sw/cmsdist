## INCLUDE rocm-config
### RPM external rocr-runtime %{rocm_version_num}
Requires: rocm-core zlib libxml2 rocprofiler-register numactl rocm-llvm
%define ROCMPreBuild export ROCM_PATH=$ROCM_LLVM_ROOT; export ROCM_DEVICE_LIB_PATH=$ROCM_LLVM_ROOT/amdgcn/bitcode
%define cmake_args -DCMAKE_CXX_COMPILER=$ROCM_LLVM_ROOT/lib/llvm/bin/clang++ -DBUILD_SHARED_LIBS=ON -DCMAKE_C_FLAGS="-I${NUMACTL_ROOT}/include" -DCMAKE_CXX_FLAGS="-I${NUMACTL_ROOT}/include --rocm-path=$ROCM_LLVM_ROOT"
%define ROCMPostPost %{relocateConfig}/lib64/cmake/hsakmt/hsakmtTargets.cmake
## INCLUDE rocm-systems-build
