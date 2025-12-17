### RPM external g4vg v1.0.5
%define g4vg_gitversion %(echo %{realversion} | sed -e 's|^v||;s|-.*||')
%define tag d377c26ea725d35d222f8b8dbd1094d0bb9a7a76
Source: git+https://github.com/celeritas-project/g4vg?obj=main/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz

%define package_build_flags -Wall -Wextra -pedantic
## INCLUDE geant4-deps
Requires: geant4 vecgeom

%prep
%setup -n %{n}-%{realversion}

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
  -DCMAKE_C_FLAGS="%{build_flags}" \
  -DCMAKE_STATIC_LIBRARY_CXX_FLAGS="%{build_flags}" \
  -DCMAKE_STATIC_LIBRARY_C_FLAGS="%{build_flags}" \
  -DCMAKE_PREFIX_PATH="%{cmake_prefix_path}" \
  -DCMAKE_POSITION_INDEPENDENT_CODE=ON \
  -DBUILD_SHARED_LIBS=ON

make %{makeprocesses} VERBOSE=1

%install
cd ../build
make %{makeprocesses} install VERBOSE=1

%post
%{relocateConfig}lib64/cmake/G4VG/G4VGConfig.cmake
