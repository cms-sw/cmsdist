### RPM external geant4 11.0.0
## INCLUDE compilation_flags
%define tag 1669bc931992fd477f5a0270453781169922d8ea
%define branch cms/v%{realversion}
%define github_user cms-externals
Source: git+https://github.com/%github_user/%{n}.git?obj=%{branch}/%{tag}&export=%{n}.%{realversion}&output=/%{n}.%{realversion}-%{tag}.tgz

BuildRequires: cmake gmake

Requires: clhep
Requires: expat
Requires: xerces-c
Requires: vecgeom
Requires: zlib

%define keep_archives true

%prep
%setup -n %{n}.%{realversion}

%build

SOEXT=so
if [ $(uname) = Darwin ]; then
  SOEXT=dylib
fi

rm -rf ../build
mkdir ../build
cd ../build
export VecGeom_DIR=${VECGEOM_ROOT}/lib/cmake/VecGeom 

cmake ../%{n}.%{realversion} \
  -DCMAKE_CXX_COMPILER="g++" \
%if "%{?arch_build_flags}"
  -DCMAKE_CXX_FLAGS="-fPIC %{arch_build_flags}" \
  -DCMAKE_STATIC_LIBRARY_CXX_FLAGS="-fPIC %{arch_build_flags}" \
  -DCMAKE_STATIC_LIBRARY_C_FLAGS="-fPIC %{arch_build_flags}" \
%else
  -DCMAKE_CXX_FLAGS="-fPIC" \
  -DCMAKE_STATIC_LIBRARY_CXX_FLAGS="-fPIC" \
  -DCMAKE_STATIC_LIBRARY_C_FLAGS="-fPIC" \
%endif
  -DCMAKE_INSTALL_PREFIX:PATH="%i" \
  -DCMAKE_INSTALL_LIBDIR="lib" \
  -DCMAKE_BUILD_TYPE=Release \
  -DGEANT4_USE_GDML=ON \
  -DGEANT4_BUILD_CXXSTD:STRING="17" \
  -DGEANT4_BUILD_TLS_MODEL:STRING="global-dynamic" \
  -DGEANT4_ENABLE_TESTING=OFF \
  -DGEANT4_BUILD_VERBOSE_CODE=OFF \
  -DGEANT4_USE_USOLIDS="all" \
  -DBUILD_SHARED_LIBS=ON \
  -DBUILD_STATIC_LIBS=ON \
  -DGEANT4_INSTALL_EXAMPLES=OFF \
  -DGEANT4_USE_SYSTEM_CLHEP=ON \
  -DGEANT4_USE_SYSTEM_EXPAT=ON \
  -DCMAKE_PREFIX_PATH="${XERCES_C_ROOT};${CLHEP_ROOT};${EXPAT_ROOT};${ZLIB_ROOT};${VECGEOM_ROOT}" \
  -DGEANT4_USE_SYSTEM_ZLIB=ON \
  -DGEANT4_BUILD_MULTITHREADED=ON

make %makeprocesses VERBOSE=1

%install

cd ../build
make install

mkdir -p %i/lib/archive
cd %i/lib/archive
find %i/lib -name "*.a" -exec ar x {} \;
ar rcs libgeant4-static.a *.o
find . -name "*.o" -delete

%post
%{relocateConfig}lib/Geant4-*/*.cmake
%{relocateConfig}bin/geant4-config
%{relocateConfig}bin/geant4.*
%{relocateConfig}share/Geant4-*/geant4make/geant4make.*
