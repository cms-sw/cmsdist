## INCLUDE rocm-config
### RPM external amdsmi %{rocm_version_num}

Source: %{rocm_systems_source}
Requires: rocm-core python3

%prep
%setup -q -n rocm-systems

%build

cmake \
  -S %{_builddir}/rocm-systems/projects/%{n} \
  -B %{_builddir}/build \
  -DCMAKE_INSTALL_PREFIX=%{i} \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_PREFIX_PATH="%{cmake_prefix_path}" \
  -DBUILD_TESTING=OFF

make -C %{_builddir}/build %{makeprocesses}
%install
make -C %{_builddir}/build %{makeprocesses} install
