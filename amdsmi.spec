## INCLUDE rocm-config
### RPM external amdsmi %{rocm_version_num}
Requires: rocm-core python3
%define cmake_args -DBUILD_TESTING=OFF
## INCLUDE rocm-systems-build
