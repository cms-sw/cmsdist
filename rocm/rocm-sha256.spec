## INCLUDE rocm/flags
### RPM external rocm-sha256 %{rocm_version_num}
%define rocm_project_dir shared
%define rocm_project sha256
# Upstream currently supplies build targets only. Install the PIC archive,
# headers and an imported target for consumers built in separate prefixes.
Source1: rocm/sha256-config.cmake
%define ROCMPreBuild echo 'install(TARGETS rocm-sha256 ARCHIVE DESTINATION lib)' >> CMakeLists.txt
%define ROCMPostInstall \
  mkdir -p %{i}/lib/cmake/rocm-sha256 %{i}/include \
  cp %{_builddir}/build/librocm-sha256.a %{i}/lib/ \
  cp -r include/rocm %{i}/include/ \
  cp %{SOURCE1} %{i}/lib/cmake/rocm-sha256/rocm-sha256-config.cmake
## INCLUDE rocm/systems-build
