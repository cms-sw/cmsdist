## INCLUDE rocm-config
### RPM external aqlprofile %{rocm_version_num}

Source: %{rocm_systems_source}
Requires: rocm-core rocr-runtime
%prep
%setup -q -n rocm-systems/projects/%{n}

%build

cmake \
  -S %{_builddir}/rocm-systems/projects/%{n} \
  -B %{_builddir}/build \
  -DCMAKE_INSTALL_PREFIX=%{i} \
  -DCMAKE_BUILD_TYPE=%{cmake_build_type} \
  -DCMAKE_PREFIX_PATH=%{cmake_prefix_path}

make -C %{_builddir}/build %{makeprocesses} VERBOSE=1

%install
make -C %{_builddir}/build %{makeprocesses} install VERBOSE=1
