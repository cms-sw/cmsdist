### RPM external geant4 10.7.2
## INCLUDE compilation_flags
%define use_vecgeom 1
%define tag %{realversion}
%define branch geant4-10.7-release
%define github_user Geant4
Source: git+https://github.com/%github_user/%{n}.git?obj=%{branch}/v%{tag}&export=%{n}.%{realversion}&output=/%{n}.%{realversion}-%{tag}.tgz

BuildRequires: cmake gmake

Requires: clhep
Requires: expat
Requires: xerces-c
%if %{use_vecgeom}
Requires: vecgeom
%endif
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
%if %{use_vecgeom}
export VecGeom_DIR=${VECGEOM_ROOT}/lib/cmake/VecGeom 
%endif

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
  -DCMAKE_AR=$(which gcc-ar) \
  -DCMAKE_RANLIB=$(which gcc-ranlib) \
  -DCMAKE_INSTALL_PREFIX:PATH="%i" \
  -DCMAKE_CXX_STANDARD:STRING="17" \
  -DCMAKE_BUILD_TYPE=Release \
  -DGEANT4_USE_GDML=ON \
  -DGEANT4_BUILD_TLS_MODEL:STRING="global-dynamic" \
  -DGEANT4_ENABLE_TESTING=OFF \
  -DGEANT4_BUILD_VERBOSE_CODE=OFF \
%if %{use_vecgeom}
  -DGEANT4_USE_USOLIDS="all" \
%endif
  -DBUILD_SHARED_LIBS=ON \
  -DBUILD_STATIC_LIBS=ON \
  -DGEANT4_INSTALL_EXAMPLES=OFF \
  -DGEANT4_USE_SYSTEM_CLHEP=ON \
  -DGEANT4_USE_SYSTEM_EXPAT=ON \
  -DCMAKE_PREFIX_PATH="${XERCES_C_ROOT};${CLHEP_ROOT};${EXPAT_ROOT};${ZLIB_ROOT};${VECGEOM_ROOT};${VECCORE_ROOT}" \
  -DGEANT4_USE_SYSTEM_ZLIB=ON \
  -DGEANT4_BUILD_MULTITHREADED=ON

make %makeprocesses VERBOSE=1

%install

cd ../build
make install

mkdir -p %i/lib64/archive
cd %i/lib64/archive
find %i/lib64 -name "*.a" -exec gcc-ar x {} \;
gcc-ar rcs libgeant4-static.a *.o
find . -name "*.o" -delete

%post
%{relocateConfig}lib64/Geant4-*/*.cmake
%{relocateConfig}bin/geant4-config
%{relocateConfig}bin/geant4.*
%{relocateConfig}share/Geant4-*/geant4make/geant4make.*
