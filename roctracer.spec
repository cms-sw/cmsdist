## INCLUDE rocm-config
### RPM external roctracer %{rocm_version_num}

Source0: %{rocm_systems_source}%{n}.tar.gz
Requires: rocr-runtime hip

%prep
%setup -q -n %{n}

%build
sed -i 's/add_subdirectory(test)/# add_subdirectory(test)/' %{_builddir}/%{n}/CMakeLists.txt

cmake \
  -S %{_builddir}/%{n} \
  -B %{_builddir}/build \
  -DCMAKE_INSTALL_PREFIX=%{i} \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_PREFIX_PATH="%{cmake_prefix_path}" \
  -DBUILD_TESTS=OFF

make -C %{_builddir}/build %{makeprocesses}

%install
make -C %{_builddir}/build %{makeprocesses} install
