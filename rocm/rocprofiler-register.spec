## INCLUDE rocm/flags
### RPM external rocprofiler-register %{rocm_version_num}
Requires: fmt
%define ROCMPreCMake sed -i -e 's|add_subdirectory(external)|find_package(fmt REQUIRED)\\nadd_subdirectory(external)|' CMakeLists.txt ; sed -i -e 's|CMAKE_CXX_STANDARD  *17|CMAKE_CXX_STANDARD %{cms_cxx_standard}|' cmake/rocprofiler_register_options.cmake
%define cmake_args -DROCPROFILER_REGISTER_BUILD_FMT=OFF
## INCLUDE rocm/systems-build
