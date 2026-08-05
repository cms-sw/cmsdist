## INCLUDE rocm-config
### RPM external roctracer %{rocm_version_num}
Requires: rocr-runtime rocm-hip rocm-comgr
BuildRequires: py3-CppHeaderParser
%define ROCMPreCMake sed -i 's/add_subdirectory(test)/# add_subdirectory(test)/' %{_builddir}/rocm-systems/projects/%{n}/CMakeLists.txt
%define cmake_args -DBUILD_TESTS=OFF
## INCLUDE rocm-systems-build
