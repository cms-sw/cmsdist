## INCLUDE rocm-config
### RPM external rocblas %{rocm_version_num}
Requires: roctracer hipblaslt hipblas-common python3 rocr-runtime msgpack-cxx boost rocminfo rocm-llvm rocm-comgr
%define cmake_args -DCMAKE_CXX_FLAGS="-I$BOOST_ROOT/include --rocm-path=$ROCM_LLVM_ROOT/amdgcn/bitcode" -DROCTX_PATH=$ROCTRACER_ROOT/lib64
%define ROCMPostPost %{relocateConfig}/lib/rocblas/library/TensileManifest.txt
## INCLUDE rocm-libraries-build
