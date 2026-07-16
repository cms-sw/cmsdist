## INCLUDE rocm-config
### RPM external roctracer %{rocm_version_num}
Source: %{rocm_systems_source}
Requires: rocr-runtime rocm-hip rocm-comgr
BuildRequires: py3-CppHeaderParser

%prep
%setup -q -n rocm-systems/projects/%{n}

%build
sed -i 's/add_subdirectory(test)/# add_subdirectory(test)/' %{_builddir}/rocm-systems/projects/%{n}/CMakeLists.txt

cmake \
  -S %{_builddir}/rocm-systems/projects/%{n} \
  -B %{_builddir}/build \
  -DCMAKE_INSTALL_PREFIX=%{i} \
  -DCMAKE_BUILD_TYPE=%{cmake_build_type} \
  -DCMAKE_PREFIX_PATH="%{cmake_prefix_path}" \
  -DBUILD_TESTS=OFF

make -C %{_builddir}/build %{makeprocesses} VERBOSE=1

%install
make -C %{_builddir}/build %{makeprocesses} install VERBOSE=1
