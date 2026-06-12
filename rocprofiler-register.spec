## INCLUDE rocm-config
### RPM external rocprofiler-register %{rocm_version_num}
## INCLUDE cpp-standard

Source0: %{rocm_systems_source}

BuildRequires: gmake cmake
Requires: fmt
AutoReq: no

%prep
%setup -q -n rocm-systems

%build
sed -i -e 's|add_subdirectory(external)|find_package(fmt REQUIRED)\nadd_subdirectory(external)|' %{_builddir}/rocm-systems/projects/%{n}/CMakeLists.txt
%if %{cms_cxx_standard} != 17
grep -q 'CMAKE_CXX_STANDARD  *17' %{_builddir}/rocm-systems/projects/%{n}/cmake/rocprofiler_register_options.cmake
sed -i -e 's|CMAKE_CXX_STANDARD  *17|CMAKE_CXX_STANDARD %{cms_cxx_standard}|' %{_builddir}/rocm-systems/projects/%{n}/cmake/rocprofiler_register_options.cmake
%endif

cmake \
  -S %{_builddir}/rocm-systems/projects/%{n} \
  -B %{_builddir}/build \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_INSTALL_PREFIX=%{i} \
  -DCMAKE_CXX_STANDARD=%{cms_cxx_standard} \
  -DCMAKE_VERBOSE_MAKEFILE=TRUE \
  -DROCPROFILER_REGISTER_BUILD_FMT=OFF \
  -DCMAKE_PREFIX_PATH="${FMT_ROOT}"

make -C %{_builddir}/build %{makeprocesses} VERBOSE=1

%install
make -C %{_builddir}/build %{makeprocesses} install
