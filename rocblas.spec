## INCLUDE rocm-config
### RPM external rocblas %{rocm_version_num}
Requires: roctracer hipblaslt hipblas-common python3 rocr-runtime msgpack-cxx boost rocminfo rocm-llvm comgr
%define cmake_args -DCMAKE_CXX_FLAGS="-I$BOOST_ROOT/include --rocm-path=$ROCM_LLVM_ROOT/amdgcn/bitcode"
## INCLUDE rocm-libraries-build-new
%post
%{relocateConfig}/lib/rocblas/library/TensileManifest.txt
