### RPM external rocprofiler-register 7.2.2
## INCLUDE cpp-standard

# ROCm branch, e.g. 5.6, 6.2
%define rocm_branch %(echo %{realversion} | cut -d. -f1-2)

# git branch, tag and directory name for rocprofiler-register
%define rocprofiler_register_branch release/rocm-rel-%{rocm_branch}
%define rocprofiler_register_tag    rocm-%{realversion}
%define rocprofiler_register_pkg    rocprofiler-register-%{rocprofiler_register_tag}

Source0: git+https://github.com/ROCm/rocprofiler-register.git?obj=%{rocprofiler_register_branch}/%{rocprofiler_register_tag}&export=%{rocprofiler_register_pkg}&submodules=1&output=/%{rocprofiler_register_pkg}.tgz

BuildRequires: gmake cmake
Requires: fmt
AutoReq: no

%prep
mkdir src
tar xavf %{SOURCE0} -C src

%build
sed -i -e 's|add_subdirectory(external)|find_package(fmt REQUIRED)\nadd_subdirectory(external)|' src/%{rocprofiler_register_pkg}/CMakeLists.txt
%if %{cms_cxx_standard} != 17
grep -q 'CMAKE_CXX_STANDARD  *17' src/%{rocprofiler_register_pkg}/cmake/rocprofiler_register_options.cmake
sed -i -e 's|CMAKE_CXX_STANDARD  *17|CMAKE_CXX_STANDARD %{cms_cxx_standard}|' src/%{rocprofiler_register_pkg}/cmake/rocprofiler_register_options.cmake
%endif

mkdir -p build/rocprofiler-register
cd build/rocprofiler-register
cmake ../../src/%{rocprofiler_register_pkg} \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_INSTALL_PREFIX=%{i} \
  -DCMAKE_CXX_STANDARD=%{cms_cxx_standard} \
  -DCMAKE_VERBOSE_MAKEFILE=TRUE \
  -DROCPROFILER_REGISTER_BUILD_FMT=OFF \
  -DCMAKE_PREFIX_PATH="${FMT_ROOT}"
make all %{makeprocesses}

%install
cd build/rocprofiler-register
make install
