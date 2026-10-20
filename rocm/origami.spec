## INCLUDE rocm/flags
### RPM external origami %{rocm_version_num}
%define rocm_project_dir shared
%define cmake_args -DORIGAMI_BUILD_TESTING=OFF
## INCLUDE rocm/libraries-build
