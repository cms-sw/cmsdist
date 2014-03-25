### RPM external geant4 10.00.p01

Source0: http://geant4.cern.ch/support/source/%{n}.%{realversion}.tar.gz

BuildRequires: cmake

Requires: clhep
Requires: expat
Requires: xerces-c

Patch0: geant4-10.0-no-banner
Patch1: geant4-10.0.p01-dynamic-tls

%if "%{?cms_cxx:set}" != "set"
%define cms_cxx g++
%endif

%prep
%setup -n %{n}.%{realversion}

%patch0 -p1
%patch1 -p1

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
  -DCMAKE_INSTALL_PREFIX:PATH="%i" \
  -DCMAKE_INSTALL_LIBDIR="lib" \
  -DCMAKE_BUILD_TYPE=Release \
  -DGEANT4_USE_GDML=ON \
  -DGEANT4_BUILD_CXXSTD:STRING="c++11" \
  -DGEANT4_ENABLE_TESTING=OFF \
  -DBUILD_SHARED_LIBS=ON \
  -DXERCESC_ROOT_DIR:PATH="${XERCES_C_ROOT}" \
  -DCLHEP_ROOT_DIR:PATH="$CLHEP_ROOT" \
  -DEXPAT_INCLUDE_DIR:PATH="$EXPAT_ROOT/include" \
  -DEXPAT_LIBRARY:FILEPATH="$EXPAT_ROOT/lib/libexpat.$SOEXT" \
  -DBUILD_STATIC_LIBS=ON \
  -DGEANT4_INSTALL_EXAMPLES=OFF \
  -DGEANT4_USE_SYSTEM_CLHEP=OFF \
  -DGEANT4_BUILD_MULTITHREADED=OFF \

make %makeprocesses VERBOSE=1

%install

cd ../build
make install

%post
%{relocateConfig}lib/Geant4-*/Geant4Config.cmake
