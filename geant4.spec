### RPM external geant4 11.1.1
## INCLUDE compilation_flags
## INCLUDE compilation_flags_lto
%define use_vecgeom 1
%define tag 35f304cde19a3e2dfe3bb941d4fc76c2fe45fa26
%define branch cms/v%{realversion}
%define github_user cms-externals
Source: git+https://github.com/%github_user/%{n}.git?obj=%{branch}/%{tag}&export=%{n}.%{realversion}&output=/%{n}.%{realversion}-%{tag}.tgz

BuildRequires: cmake gmake

Requires: clhep
Requires: expat
Requires: xerces-c
%if %{use_vecgeom}
Requires: vecgeom
%endif
Requires: zlib

%define keep_archives true
%define build_flags -fPIC %{?arch_build_flags} %{?lto_build_flags} %{?pgo_build_flags}

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
  -DCMAKE_CXX_FLAGS="%{build_flags}" \
  -DCMAKE_STATIC_LIBRARY_CXX_FLAGS="%{build_flags}" \
  -DCMAKE_STATIC_LIBRARY_C_FLAGS="%{build_flags}" \
  -DCMAKE_AR=$(which gcc-ar) \
  -DCMAKE_RANLIB=$(which gcc-ranlib) \
  -DCMAKE_INSTALL_PREFIX:PATH="%i" \
  -DCMAKE_CXX_STANDARD:STRING="17" \
  -DCMAKE_BUILD_TYPE=Release \
  -DGEANT4_USE_GDML=ON \
  -DGEANT4_BUILD_TLS_MODEL:STRING="global-dynamic" \
  -DGEANT4_ENABLE_TESTING=OFF \
  -DGEANT4_BUILD_VERBOSE_CODE=OFF \
  -DGEANT4_BUILD_BUILTIN_BACKTRACE=OFF \
%if %{use_vecgeom}
  -DGEANT4_USE_USOLIDS="all" \
%endif
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

mkdir -p %i/lib64/archive
cd %i/lib64/archive
find %i/lib64 -name "*.a" -exec gcc-ar x {} \;
gcc-ar rcs libgeant4-static.a *.o
find . -name "*.o" -delete

%if "%{?pgo_build_flags}"
sed -ire 's| +(-fprofile-[^ ]+ )+||' %{i}/lib64/Geant4-*/Geant4Config.cmake %{i}/bin/geant4-config
%endif

%post
%{relocateCmsFiles} $(find $RPM_INSTALL_PREFIX/%{pkgrel} -name '*.cmake')
%{relocateConfig}bin/geant4-config
%{relocateConfig}bin/geant4.*
%{relocateConfig}share/Geant4*/geant4make/geant4make.*
