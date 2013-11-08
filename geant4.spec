### RPM external geant4 9.6ref10
%define mic %(case %cmsplatf in (*_mic_*) echo true;; (*) echo false;; esac)
%if "%mic" == "true"
Requires: icc
%endif

#Source0: http://geant4.cern.ch/support/source/%{n}.%{realversion}.tar.gz
Source0: http://cern.ch/vnivanch/%{n}.%{realversion}.tar.gz

%if "%mic" != "true"
BuildRequires: cmake
%endif

Requires: clhep
Requires: expat
Requires: xerces-c

Patch0: geant4-10.0-no-banner

%if "%{?cms_cxx:set}" != "set"
%define cms_cxx g++
%endif

%if "%{?cms_cxxflags:set}" != "set"
%define cms_cxxflags -std=c++0x
%endif

%prep
%setup -n %{n}

%patch0 -p1

%build

SOEXT=so
if [ $(uname) = Darwin ]; then
  SOEXT=dylib
fi
rm -rf ../build
mkdir ../build
cd ../build

cmake ../%{n} \
  -DCMAKE_INSTALL_PREFIX:PATH="%i" \
  -DCMAKE_INSTALL_LIBDIR="lib" \
  -DCMAKE_BUILD_TYPE=Release \
  -DGEANT4_USE_SYSTEM_CLHEP=ON \
  -DGEANT4_USE_GDML=ON \
  -DGEANT4_BUILD_MULTITHREADED=ON \
  -DBUILD_SHARED_LIBS=ON \
  -DBUILD_STATIC_LIBS=OFF \
  -DGEANT4_INSTALL_EXAMPLES=OFF \
  -DGEANT4_ENABLE_TESTING=OFF \
  -DXERCESC_ROOT_DIR:PATH="${XERCES_C_ROOT}" \
  -DCLHEP_ROOT_DIR:PATH="$CLHEP_ROOT" \
  -DEXPAT_INCLUDE_DIR:PATH="$EXPAT_ROOT/include" \
  -DEXPAT_LIBRARY:FILEPATH="$EXPAT_ROOT/lib/libexpat.$SOEXT" \
%if "%mic" == "true"
  -DCMAKE_CXX_COMPILER="icpc" \
  -DCMAKE_CXX_FLAGS="-mmic" \
  -DCMAKE_C_COMPILER="icc" \
  -DCMAKE_C_FLAGS="-mmic"
%else
  -DCMAKE_CXX_COMPILER="%cms_cxx" \
  -DCMAKE_CXX_FLAGS="%cms_cxxflags"
%endif

make %makeprocesses VERBOSE=1

%install

cd ../build
make install

%post
%{relocateConfig}lib/Geant4-*/Geant4Config.cmake
