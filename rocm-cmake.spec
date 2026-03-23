### RPM external rocm-cmake 7.10

Source0: https://github.com/ROCm/rocm-cmake/archive/refs/tags/therock-%{realversion}.tar.gz

BuildRequires: cmake

%prep
%setup -q -n rocm-cmake-therock-7.10

%build
mkdir -p build
cd build
cmake .. \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_INSTALL_PREFIX=%{i}

%install
cd build
make install
