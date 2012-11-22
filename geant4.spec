### RPM external geant4 9.6.cand01

%define downloadv %(echo %v | cut -d- -f1)
Source0: http://cern.ch/vnivanch/verification/verification/hadronic/geant4.9.6.cand01+.tar.gz

BuildRequires: cmake

Requires: clhep
Requires: expat

Patch0: geant4.9.5.p01-no-banner

%if "%{?cms_cxx:set}" != "set"
%define cms_cxx g++
%endif

%if "%{?cms_cxxflags:set}" != "set"
%define cms_cxxflags -std=c++0x
%endif

%prep
%setup -n %n

%patch0 -p1

%build

SOEXT=so
if [ $(uname) = Darwin ]; then
  export MACOSX_DEPLOYMENT_TARGET="10.4"
  SOEXT=dylib
fi

mkdir ../build
cd ../build

cmake ../%n \
  -DCMAKE_CXX_COMPILER="%cms_cxx" \
  -DCMAKE_CXX_FLAGS="%cms_cxxflags" \
  -DCMAKE_INSTALL_PREFIX:PATH="%i" \
  -DCMAKE_INSTALL_LIBDIR="lib" \
  -DCMAKE_BUILD_TYPE=Release \
  -DGEANT4_USE_SYSTEM_CLHEP=ON \
  -DCLHEP_ROOT_DIR:PATH="$CLHEP_ROOT" \
  -DEXPAT_INCLUDE_DIR:PATH="$EXPAT_ROOT/include" \
  -DEXPAT_LIBRARY:PATH="$EXPAT_ROOT/lib/libexpat.$SOEXT" \

make %makeprocesses VERBOSE=1

%install

cd ../build
make install

# Move headers from ../include/Geant4 to ../include
tar -C %i/include/Geant4 -cf - . | tar -C %i/include -xf -
rm -rf %i/include/Geant4
