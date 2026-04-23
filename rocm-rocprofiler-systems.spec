## INCLUDE rocm-config
### RPM external rocm-rocprofiler-systems %{rocm_version_num}

Source0: git+https://github.com/akritkbehera/rocprofiler-systems.git?obj=release/rocm-rel-7.2/%{rocm_version}&export=%{n}&submodules=1&output=/%{n}.tar.gz
Requires: rocm-core rocr-runtime cmake rocm-cmake rocprofiler roctracer hip libxml2
Requires: libunwind sqlite rocm-rocprofiler-sdk amdsmi flex bison bz2lib
Provides: libbz2.so.1()(64bit)

%prep
%setup -q -n %{n}

%build

cmake \
  -B %{_builddir}/build \
  -S %{_builddir}/%{n} \
  -DCMAKE_INSTALL_PREFIX=%{i} \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_PREFIX_PATH="%{cmake_prefix_path}" \
  -DROCPROFSYS_USE_PYTHON=ON \
  -DROCPROFSYS_BUILD_DYNINST=ON \
  -DROCPROFSYS_BUILD_TBB=ON \
  -DROCPROFSYS_BUILD_BOOST=ON \
  -DROCPROFSYS_BUILD_LIBIBERTY=ON \
  -DROCPROFSYS_BUILD_ELFUTILS=ON \
  -DROCPROFSYS_BUILD_EXAMPLES=OFF \
  -DROCPROFSYS_BUILD_TESTING=OFF \
  -DROCPROFSYS_USE_PAPI=OFF


cmake --build %{_builddir}/build --parallel %{makeprocesses}

%install
cmake --build %{_builddir}/build --target install
