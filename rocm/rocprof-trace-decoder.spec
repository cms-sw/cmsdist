## INCLUDE rocm/flags
### RPM external rocprof-trace-decoder %{rocm_version_num}
Requires: rocm-comgr python3
%define ROCMPrePost %{relocateConfig}lib/cmake/rocprof-trace-decoder/rocprof-trace-decoder-targets.cmake
## INCLUDE rocm/systems-build
