### RPM external geant4-parfullcms 2014.01.27

%define realname ParFullCMS

Source0: http://davidlt.web.cern.ch/davidlt/vault/%{realname}.%{realversion}.tar.bz2

BuildRequires: cmake
Requires: geant4
Requires: geant4data

%prep
%setup -n %{realname}

%build

mkdir build-ParFullCMS
cd build-ParFullCMS

cmake .. \
  -DCMAKE_CXX_COMPILER="g++" \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_INSTALL_PREFIX:PATH="%i" \
  -DCMAKE_INSTALL_LIBDIR="lib" \
  -DCMAKE_BUILD_TYPE=Release \
  -DBUILD_SHARED_LIBS=OFF \
  -DBUILD_STATIC_LIBS=ON \
  -DGeant4_USE_FILE=${GEANT4_ROOT}

make %{makeprocesses} VERBOSE=1

%install

cd build-ParFullCMS
make install
# bla bla
