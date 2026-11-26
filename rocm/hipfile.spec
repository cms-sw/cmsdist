## INCLUDE rocm/flags
### RPM external hipfile %{rocm_version_num}
Requires: rocm-hip rocm-core rocr-runtime rocm-comgr rocprofiler-register
%define cmake_args -DROCM_VERSION="%{rocm_version_num}.0"
## INCLUDE rocm/systems-build
