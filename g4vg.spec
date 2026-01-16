### RPM external g4vg 1.0.6
Source: https://github.com/celeritas-project/g4vg/releases/download/v%{realversion}/g4vg-%{realversion}.tar.gz

%define package_build_flags -Wall -Wextra -pedantic
## INCLUDE geant4-deps
Requires: geant4 vecgeom

%prep
%setup -c -n %{n}-%{realversion}

%build

rm -rf ../build
mkdir ../build
cd ../build

cmake ../%{n}-%{realversion} \
  -DCMAKE_INSTALL_PREFIX=%{i} \
  -DCMAKE_CXX_STANDARD:STRING="%{cms_cxx_standard}" \
  -DCMAKE_AR=$(which gcc-ar) \
  -DCMAKE_RANLIB=$(which gcc-ranlib) \
  -DCMAKE_BUILD_TYPE=%{cmake_build_type} \
  -DCMAKE_CXX_FLAGS="%{build_flags}" \
  -DCMAKE_STATIC_LIBRARY_CXX_FLAGS="%{build_flags}" \
  -DCMAKE_PREFIX_PATH="%{cmake_prefix_path}" \
  -DBUILD_SHARED_LIBS=OFF \
  -DCMAKE_POSITION_INDEPENDENT_CODE=ON \
  -DG4VG_BUILD_TESTS=OFF \
  -DG4VG_DEBUG=OFF

make %{makeprocesses} VERBOSE=1

%install
cd ../build
make %{makeprocesses} install VERBOSE=1

%post
%{relocateConfig}lib64/cmake/G4VG/G4VGConfig.cmake
