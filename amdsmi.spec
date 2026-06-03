## INCLUDE rocm-config
### RPM external amdsmi %{rocm_version_num}

Source: https://github.com/ROCm/amdsmi/archive/refs/tags/%{rocm_version}.tar.gz
Requires: rocm-core python3

%prep
%setup -q -n amdsmi-%{rocm_version}

%build

cmake \
  -S %{_builddir}/amdsmi-%{rocm_version} \
  -B %{_builddir}/build \
  -DCMAKE_INSTALL_PREFIX=%{i} \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_PREFIX_PATH="%{cmake_prefix_path}" \
  -DBUILD_TESTING=OFF

make -C %{_builddir}/build %{makeprocesses}
%install
make -C %{_builddir}/build %{makeprocesses} install
