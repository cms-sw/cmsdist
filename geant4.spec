### RPM external geant4 10.0.cand00a

Source0: http://cern.ch/vnivanch/geant4.10.0cand00a.tar.gz

BuildRequires: cmake

Requires: clhep
Requires: expat
Requires: xerces-c

Patch0: geant4-10.0-no-banner

%if "%{?cms_cxx:set}" != "set"
%define cms_cxx g++
%endif

%prep
%setup -n %{n}

%patch0 -p1

%build

SOEXT=so
if [ $(uname) = Darwin ]; then
  SOEXT=dylib
fi

mkdir ../build
cd ../build

cmake ../%{n} \
  -DCMAKE_CXX_COMPILER="%cms_cxx" \
  -DCMAKE_INSTALL_PREFIX:PATH="%i" \
  -DCMAKE_INSTALL_LIBDIR="lib" \
  -DCMAKE_BUILD_TYPE=Release \
  -DGEANT4_USE_SYSTEM_CLHEP=ON \
  -DCLHEP_ROOT_DIR:PATH="$CLHEP_ROOT" \
  -DGEANT4_USE_GDML=ON \
  -DGEANT4_BUILD_CXXSTD:STRING="c++11" \
  -DGEANT4_ENABLE_TESTING=OFF \
  -DBUILD_SHARED_LIBS=ON \
  -DBUILD_STATIC_LIBS=OFF \
  -DGEANT4_BUILD_MULTITHREADED=ON \
  -DXERCESC_ROOT_DIR:PATH="${XERCES_C_ROOT}" \
  -DCLHEP_ROOT_DIR:PATH="$CLHEP_ROOT" \
  -DEXPAT_INCLUDE_DIR:PATH="$EXPAT_ROOT/include" \
  -DEXPAT_LIBRARY:FILEPATH="$EXPAT_ROOT/lib/libexpat.$SOEXT" \

make %makeprocesses VERBOSE=1

%install

cd ../build
make install

# Move headers from ../include/Geant4 to ../include
tar -C %i/include/Geant4 -cf - . | tar -C %i/include -xf -
rm -rf %i/include/Geant4
