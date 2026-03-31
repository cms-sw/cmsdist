### RPM external rocm-core 7.1.0
Source: https://github.com/ROCm/rocm-systems/archive/refs/tags/rocm-%{realversion}.tar.gz
BuildRequires: cmake
Requires: python3 py3-prettytable py3-PyYAML 

%prep
%setup -q -n rocm-systems-rocm-%{realversion}

%build
mkdir -p %{_builddir}/build
cd %{_builddir}/build
cmake \
  -S %{_builddir}/rocm-systems-rocm-%{realversion}/projects/rocm-core \
  -B %{_builddir}/build \
  -DCMAKE_INSTALL_PREFIX=%{i} \
  -DROCM_VERSION="%{realversion}"

#cmake --build build --parallel %{makeprocesses}
make %{makeprocesses}
%install
#cmake --install build %{makeprocesses}
make -C %{_builddir}/build %{makeprocesses} install
