### RPM external g4tests 1.0
%define mic %(case %cmsplatf in (*_mic_*) echo true;; (*) echo false;; esac)
%if "%mic" == "true"
Requires: icc
%endif

Source0: http://cern.ch/vnivanch/ParFullCMS.tar.gz 
Patch0: g4tests-mt

%if "%mic" != "true"
BuildRequires: cmake
%endif

Requires: geant4

%if "%{?cms_cxx:set}" != "set"
%define cms_cxx g++
%endif

%if "%{?cms_cxxflags:set}" != "set"
%define cms_cxxflags -std=c++0x
%endif

%prep
%setup -n ParFullCMS
%patch0 -p0

%build

rm -rf ../build; mkdir ../build; cd ../build

cmake ../ParFullCMS -DCMAKE_INSTALL_PREFIX:PATH="%i" -DGeant4_DIR=$GEANT4_ROOT/lib*/Geant4-* -DCMAKE_BUILD_TYPE=RelWithDebInfo \
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
