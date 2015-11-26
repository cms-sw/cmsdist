### RPM external geant4-parfullcms 2015.11.26

%define realname parfullcms
%define github_user cms-externals
Source: https://github.com/%{github_user}/%{realname}/archive/%{realversion}.tar.gz

BuildRequires: cmake
Requires: geant4
Requires: geant4data

%prep
%setup -n %{realversion}

%build

mkdir build-ParFullCMS
cd build-ParFullCMS

cmake .. \
  -DCMAKE_CXX_COMPILER="g++" \
  -DCMAKE_CXX_FLAGS="-std=c++11" \
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
