### RPM external celeritas v0.4.1
## INCLUDE compilation_flags
## INCLUDE compilation_flags_lto
## INCLUDE cpp-standard
%define keep_archives true
%define celeritas_gitversion %(echo %{realversion} | sed -e 's|^v||;s|-.*||')
%define tag f9b51d72fc268bf22c5560b82d3dd3d7613a8106
Source: git+https://github.com/celeritas-project/celeritas?obj=develop/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz
BuildRequires: cmake

%define build_flags -Wall -Wextra -pedantic %{?arch_build_flags} %{?lto_build_flags} %{?pgo_build_flags}
Requires: json
Requires: geant4
Requires: vecgeom

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
  -DCMAKE_PREFIX_PATH="%{cmake_prefix_path}" \
  -DBUILD_SHARED_LIBS=OFF \
  -DCMAKE_POSITION_INDEPENDENT_CODE=ON \
  -DCELERITAS_BUILD_TESTS=OFF \
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
  -DCELERITAS_USE_VecGeom=ON

make %{makeprocesses} VERBOSE=1

%install
cd ../build
make %{makeprocesses} install VERBOSE=1

%post
%{relocateConfig}lib64/cmake/Celeritas/CeleritasConfig.cmake
