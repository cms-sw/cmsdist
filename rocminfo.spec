## INCLUDE rocm-config
### RPM external rocminfo %{rocm_version_num}

Source0: %{rocm_systems_source}/%{n}.tar.gz
Requires: rocm-core rocr-runtime
%prep
%setup -q -n %{n}
%build
cmake -B %{_builddir}/build \
  -S %{_builddir}/%{n} \
  -DCMAKE_INSTALL_PREFIX=%{i} \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_PREFIX_PATH="%{cmake_prefix_path}"

make -C %{_builddir}/build %{makeprocesses}
%install
make -C %{_builddir}/build %{makeprocesses} install
