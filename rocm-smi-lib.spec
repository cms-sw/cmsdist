## INCLUDE rocm-config
### RPM external rocm-smi-lib %{rocm_version_num}
Requires: rocm-core rocr-runtime
%define cmake_args -DBUILD_TESTING=OFF
## INCLUDE rocm-systems-build
