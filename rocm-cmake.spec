## INCLUDE rocm-config
### RPM external rocm-cmake %{rocm_version_num}
BuildRequires: cmake
Source: https://github.com/ROCm/rocm-cmake/archive/refs/tags/therock-%{rocm_version_num}.tar.gz
%prep
%setup -q -n %{n}-%{rocm_version}

%build
cmake \
  -S %{_builddir}/%{n}-%{rocm_version} \
  -B %{_builddir}/build \
  -DCMAKE_INSTALL_PREFIX=%{i} \
  -DROCM_VERSION=%{rocm_version_num}

cmake --build %{_builddir}/build --parallel %{makeprocesses}
%install
cmake --install %{_builddir}/build
