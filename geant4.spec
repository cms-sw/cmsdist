### RPM external geant4 9.6.p02

Source0: http://geant4.cern.ch/support/source/%{n}.%{realversion}.tar.gz

BuildRequires: cmake

Requires: clhep
Requires: expat
Requires: xerces-c

Patch0: geant4.9.5.p01-no-banner
Patch1: geant4-9.6p02-cms01

%define keep_archives true

%if "%{?cms_cxx:set}" != "set"
%define cms_cxx g++
%endif

%if "%{?cms_cxxflags:set}" != "set"
%define cms_cxxflags -std=c++0x
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
  -DCMAKE_CXX_FLAGS="%cms_cxxflags" \
  -DCMAKE_INSTALL_PREFIX:PATH="%i" \
  -DCMAKE_INSTALL_LIBDIR="lib" \
  -DCMAKE_BUILD_TYPE=Release \
  -DGEANT4_USE_SYSTEM_CLHEP=ON \
  -DGEANT4_USE_GDML=ON \
  -DXERCESC_ROOT_DIR:PATH="${XERCES_C_ROOT}" \
  -DCLHEP_ROOT_DIR:PATH="$CLHEP_ROOT" \
  -DEXPAT_INCLUDE_DIR:PATH="$EXPAT_ROOT/include" \
  -DEXPAT_LIBRARY:FILEPATH="$EXPAT_ROOT/lib/libexpat.$SOEXT" \
  -DBUILD_STATIC_LIBS=ON

make %makeprocesses VERBOSE=1

%install

cd ../build
make install

%post
%{relocateConfig}lib/Geant4-*/Geant4Config.cmake
