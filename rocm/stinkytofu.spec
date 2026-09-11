## INCLUDE rocm/flags
### RPM external stinkytofu %{rocm_version_num}
## INITENV +PATH PYTHON3PATH %i/lib/python%{cms_python3_major_minor_version}/dist-packages
Patch0: patches/rocm-stinkytofu-gcc14
%define rocm_project_dir shared
%define ROCMPostPrep patch -p1 -i %{PATCH0}
%define cmake_args -DSTINKYTOFU_BUILD_TESTS=OFF -DSTINKYTOFU_CODE_COVERAGE=OFF
## INCLUDE rocm/libraries-build
