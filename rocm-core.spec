## INCLUDE rocm-config
### RPM external rocm-core %{rocm_version_num}
BuildRequires: cmake
Requires: python3 py3-prettytable py3-PyYAML

Source: %{rocm_systems_source}
%prep
%setup -q -n rocm-systems/projects/%{n}

%build

cmake \
  -S %{_builddir}/rocm-systems/projects/%{n} \
  -B %{_builddir}/build \
  -DCMAKE_INSTALL_PREFIX=%{i} \
  -DCMAKE_BUILD_TYPE=%{cmake_build_type} \
  -DROCM_VERSION=%{rocm_version_num}

cmake --build %{_builddir}/build --parallel %{makeprocesses} --verbose
%install
cmake --install %{_builddir}/build --verbose
