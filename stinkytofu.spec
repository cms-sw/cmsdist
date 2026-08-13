## INCLUDE rocm-flags
### RPM external stinkytofu %{rocm_version_num}
Patch0: patches/rocm-stinkytofu-gcc14
%define rocm_libraries_dir shared
%define ROCMPostPrep patch -p1 -i %{PATCH0}
%define cmake_args -DSTINKYTOFU_BUILD_TESTS=OFF -DSTINKYTOFU_CODE_COVERAGE=OFF
## INCLUDE rocm-libraries-build
