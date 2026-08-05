## INCLUDE rocm-config
### RPM external rocdbgapi %{rocm_version_num}
Requires: rocr-runtime rocm-core rocm-comgr
%define cmake_args -DCMAKE_CXX_FLAGS="-Wno-sfinae-incomplete"
## INCLUDE rocm-systems-build
