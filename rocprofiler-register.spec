## INCLUDE rocm-config
### RPM external rocprofiler-register %{rocm_version_num}
## INCLUDE cpp-standard
BuildRequires: gmake cmake
Requires: fmt
AutoReq: no
%define ROCMPreCMake sed -i -e 's|add_subdirectory(external)|find_package(fmt REQUIRED)\\nadd_subdirectory(external)|' %{_builddir}/rocm-systems/projects/%{n}/CMakeLists.txt ; sed -i -e 's|CMAKE_CXX_STANDARD  *17|CMAKE_CXX_STANDARD %{cms_cxx_standard}|' %{_builddir}/rocm-systems/projects/%{n}/cmake/rocprofiler_register_options.cmake
%define cmake_args -DCMAKE_CXX_STANDARD=%{cms_cxx_standard} -DCMAKE_VERBOSE_MAKEFILE=TRUE -DROCPROFILER_REGISTER_BUILD_FMT=OFF -DCMAKE_PREFIX_PATH="${FMT_ROOT}"
## INCLUDE rocm-systems-build
