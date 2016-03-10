### RPM external geant4 10.02.p01
%define tag 4d4a54c7ecc74c239ae87cc26ab951a405d2b3e8 
%define branch cms/4.%{realversion}
%define github_user cms-externals
Source: git+https://github.com/%github_user/%{n}.git?obj=%{branch}/%{tag}&export=%{n}.%{realversion}&output=/%{n}.%{realversion}-%{tag}.tgz

BuildRequires: cmake

Requires: clhep
Requires: expat
Requires: xerces-c

%define keep_archives true

%if "%{?cms_cxx:set}" != "set"
%define cms_cxx g++
%endif

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

cmake ../%{n}.%{realversion} \
  -DCMAKE_CXX_COMPILER="%cms_cxx" \
  -DCMAKE_CXX_FLAGS="-fPIC" \
  -DCMAKE_INSTALL_PREFIX:PATH="%i" \
  -DCMAKE_INSTALL_LIBDIR="lib" \
  -DCMAKE_BUILD_TYPE=Release \
  -DGEANT4_USE_GDML=ON \
  -DGEANT4_BUILD_CXXSTD:STRING="c++11" \
  -DGEANT4_BUILD_TLS_MODEL:STRING="global-dynamic" \
  -DGEANT4_ENABLE_TESTING=OFF \
  -DBUILD_SHARED_LIBS=ON \
  -DXERCESC_ROOT_DIR:PATH="${XERCES_C_ROOT}" \
  -DCLHEP_ROOT_DIR:PATH="$CLHEP_ROOT" \
  -DEXPAT_INCLUDE_DIR:PATH="$EXPAT_ROOT/include" \
  -DEXPAT_LIBRARY:FILEPATH="$EXPAT_ROOT/lib/libexpat.$SOEXT" \
  -DBUILD_STATIC_LIBS=ON \
  -DGEANT4_INSTALL_EXAMPLES=OFF \
  -DGEANT4_USE_SYSTEM_CLHEP=ON \
  -DGEANT4_BUILD_MULTITHREADED=ON \
  -DCMAKE_STATIC_LIBRARY_CXX_FLAGS="-fPIC" \
  -DCMAKE_STATIC_LIBRARY_C_FLAGS="-fPIC"

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
%{relocateConfig}lib/Geant4-*/Geant4Config.cmake
