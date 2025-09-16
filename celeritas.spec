### RPM external celeritas v0.6.0
%define celeritas_gitversion %(echo %{realversion} | sed -e 's|^v||;s|-.*||')
%define tag dfa4cde7d7d65bf656b17a24c59fcc030aa6b0d9 
Source: git+https://github.com/celeritas-project/celeritas?obj=develop/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz

%define package_build_flags -Wall -Wextra -pedantic
## INCLUDE geant4-deps
## INCLUDE cuda-flags
Requires: python3 json geant4
%{!?without_cuda:Requires: cuda}

%prep
%setup -n %{n}-%{realversion}

%build

rm -rf ../build
mkdir ../build
cd ../build

cmake ../%{n}-%{realversion} \
  -DCeleritas_GIT_DESCRIBE="%{celeritas_gitversion};;" \
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
  -DCELERITAS_DEBUG=OFF \
  -DCELERITAS_USE_OpenMP=OFF \
%if 0%{!?without_cuda:1}
  -DCMAKE_CUDA_ARCHITECTURES=$(echo %{cuda_arch} | tr ' ' ';' | sed 's|;;*|;|') \
  -DCELERITAS_USE_CUDA=ON \
%else
  -DCELERITAS_USE_CUDA=OFF \
%endif
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
%{relocateConfig}lib64/cmake/G4VG/G4VGConfig.cmake
