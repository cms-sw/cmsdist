## INCLUDE rocm/flags
### RPM external profiler-hub %{rocm_version_num}
Requires: fmt sqlite spdlog json
%define rocm_project_dir profilers
%define cmake_args -DPROFILER_HUB_BUILD_TESTS=OFF
## INCLUDE rocm/systems-build
