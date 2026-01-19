### RPM external celeritas 0.6.3
Source: https://github.com/celeritas-project/celeritas/releases/download/v%{realversion}/celeritas-%{realversion}.tar.gz

%define package_build_flags -Wall -Wextra -pedantic
## INCLUDE geant4-deps
Requires: python3 json geant4 g4vg

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
  -DCMAKE_C_FLAGS="%{build_flags}" \
  -DCMAKE_STATIC_LIBRARY_CXX_FLAGS="%{build_flags}" \
  -DCMAKE_STATIC_LIBRARY_C_FLAGS="%{build_flags}" \
  -DCMAKE_PREFIX_PATH="%{cmake_prefix_path}" \
  -DBUILD_SHARED_LIBS=OFF \
  -DCMAKE_POSITION_INDEPENDENT_CODE=ON \
  -DCELERITAS_BUILD_TESTS=OFF \
  -DCELERITAS_BUILTIN_G4VG:BOOL=OFF \
  -DCELERITAS_DEBUG=OFF \
  -DCELERITAS_USE_OpenMP=OFF \
  -DCELERITAS_USE_CUDA=OFF \
  -DCELERITAS_USE_Geant4=ON \
  -DCELERITAS_USE_HIP=OFF \
  -DCELERITAS_USE_HepMC3=OFF \
  -DCELERITAS_USE_JSON=ON \
  -DCELERITAS_USE_MPI=OFF \
  -DCELERITAS_USE_ROOT=OFF \
  -DCELERITAS_USE_SWIG=OFF \
  -DCELERITAS_USE_PNG=OFF \
%if %{enable_vecgeom}
  -DCELERITAS_USE_VecGeom=ON
%else
  -DCELERITAS_USE_VecGeom=OFF
%endif

make %{makeprocesses} VERBOSE=1

%install
cd ../build
make %{makeprocesses} install VERBOSE=1

%post
%{relocateConfig}lib64/cmake/Celeritas/CeleritasConfig.cmake
