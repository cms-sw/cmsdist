## INCLUDE rocm-config
### RPM external rocm-core %{rocm_version_num}
BuildRequires: cmake
Requires: python3 py3-prettytable py3-PyYAML

Source: %{rocm_systems_source}/%{n}.tar.gz
%prep
%setup -q -n %{n}

%build
cmake \
  -S %{_builddir}/%{n} \
  -B %{_builddir}/build \
  -DCMAKE_INSTALL_PREFIX=%{i} \
  -DROCM_VERSION=%{rocm_version_num}

cmake --build %{_builddir}/build --parallel %{makeprocesses}
%install
cmake --install %{_builddir}/build
