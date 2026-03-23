### RPM external rocm-core 7.10
Source: https://github.com/ROCm/rocm-systems/releases/download/therock-%{realversion}/rocm-core.tar.gz
BuildRequires: cmake
Requires: python3 py3-prettytable py3-PyYAML 

%prep
%setup -n %{n}

%build
cmake -B build -S . -DCMAKE_INSTALL_PREFIX=%{i} -DROCM_VERSION="7.1.0" -DCMAKE_VERBOSE_MAKEFILE=1 -DCMAKE_PREFIX_PATH="%{cmake_prefix_path}"
cmake --build build --parallel %{makeprocesses}

%install
cmake --install build %{makeprocesses}
