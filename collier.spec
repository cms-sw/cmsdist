### RPM external collier 1.2.8
# Source: http://www.hepforge.org/archive/collier/%{n}-%{realversion}.tar.gz
Source: https://cmsrep.cern.ch/cmssw/download/collier/%{realversion}/%{n}-%{realversion}.tar.gz
BuildRequires: gmake cmake

%define keep_archives true

%prep
%setup -q -n COLLIER-%{realversion}
sed -i 's;add_definitions(-Dcollierdd -DSING);add_definitions(-Dcollierdd -DSING -fPIC);g' ./CMakeLists.txt

%build
rm -rf build && mkdir build && cd build
cmake ../ \
  -DCMAKE_INSTALL_PREFIX=%{i} \
  -DCMAKE_BUILD_TYPE=Release \
  -Dstatic=ON \
  -DCMAKE_Fortran_FLAGS=-fPIC

make -j1

%install
mkdir -p %{i}/lib %{i}/include
cp libcollier.a %{i}/lib
cp modules/*.mod %{i}/include/


