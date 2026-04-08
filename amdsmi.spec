## INCLUDE rocm-config
### RPM external amdsmi %{rocm_version_num}

Source0: %{rocm_systems_source}%{n}.tar.gz
Requires: rocm-core python3

%prep
%setup -q -n %{n}

%build

cmake \
  -S %{_builddir}/%{n} \
  -B %{_builddir}/build \
  -DCMAKE_INSTALL_PREFIX=%{i} \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_PREFIX_PATH="%{cmake_prefix_path}" \
  -DBUILD_TESTING=OFF

make -C %{_builddir}/build %{makeprocesses}
%install
make -C %{_builddir}/build %{makeprocesses} install
