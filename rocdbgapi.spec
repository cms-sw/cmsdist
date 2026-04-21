## INCLUDE rocm-config
### RPM external rocdbgapi %{rocm_version_num}

Source: https://github.com/ROCm/ROCdbgapi/archive/refs/tags/%{rocm_version}.tar.gz
Requires: rocr-runtime rocm-core

%prep
%setup -q -n ROCdbgapi-%{rocm_version}

%build

cmake \
  -B %{_builddir}/build \
  -S %{_builddir}/ROCdbgapi-%{rocm_version} \
  -DCMAKE_INSTALL_PREFIX=%{i} \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_PREFIX_PATH="%{cmake_prefix_path}"

make -C %{_builddir}/build %{makeprocesses} 

%install
make -C %{_builddir}/build %{makeprocesses} install
