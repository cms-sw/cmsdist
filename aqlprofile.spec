## INCLUDE rocm-config
### RPM external aqlprofile %{rocm_version}

Source: %{rocm_systems_source}/%{n}.tar.gz
Requires: rocm-core rocr-runtime
%prep
%setup -q -n %{n}

%build

cmake \
  -S %{_builddir}/%{n} \
  -B %{_builddir}/build \
  -DCMAKE_INSTALL_PREFIX=%{i} \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_PREFIX_PATH=%{cmake_prefix_path}

make -C %{_builddir}/build %{makeprocesses}

%install
make -C %{_builddir}/build %{makeprocesses} install
