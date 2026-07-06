## INCLUDE rocm-config
### RPM external hipblas %{rocm_version_num}
Requires: roctracer hipblas-common python3 rocr-runtime rocblas rocsparse rocsolver rocm-comgr
%define cmake_args -DCMAKE_CXX_FLAGS="-I$BOOST_ROOT/include"
## INCLUDE rocm-libraries-build
