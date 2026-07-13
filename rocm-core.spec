## INCLUDE rocm-config
### RPM external rocm-core %{rocm_version_num}
BuildRequires: cmake
Requires: python3 py3-prettytable py3-PyYAML
%define cmake_args -DROCM_VERSION="%{rocm_version_num}.0"
## INCLUDE rocm-systems-build
