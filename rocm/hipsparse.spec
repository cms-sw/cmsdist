## INCLUDE rocm/flags
### RPM external hipsparse %{rocm_version_num}
Requires: rocprim rocsparse
%define cmake_args -DHIPSPARSE_ENABLE_THEROCK=ON -DHIPSPARSE_ENABLE_CLIENT=OFF
## INCLUDE rocm/libraries-build
