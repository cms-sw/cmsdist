### RPM external gbl V03-01-01
## INCLUDE cpp-standard
%define tag 59c2d99ea96bc739321fd251096504c91467be24
Source: git+https://gitlab.desy.de/claus.kleinwort/general-broken-lines.git?obj=main/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz
Source99: scram-tools.file/tools/eigen/env

BuildRequires: cmake
Requires: eigen

%prep
%setup -q -n %{n}-%{realversion}
grep -q 'CMAKE_CXX_STANDARD  *11' cpp/CMakeLists.txt
sed -i -e 's|CMAKE_CXX_STANDARD  *11|CMAKE_CXX_STANDARD %{cms_cxx_standard}|' cpp/CMakeLists.txt

%build
rm -rf build
mkdir build
cd build
source %{_sourcedir}/env

cmake ../cpp \
  -DCMAKE_INSTALL_PREFIX=%{i} \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_VERBOSE_MAKEFILE=ON \
  -DEIGEN3_INCLUDE_DIR=${EIGEN_ROOT}/include/eigen3 \
  -DSUPPORT_ROOT=False \
%ifarch x86_64
  -DCMAKE_CXX_FLAGS="$CMS_EIGEN_CXX_FLAGS -msse3"
%else
  -DCMAKE_CXX_FLAGS="$CMS_EIGEN_CXX_FLAGS"
%endif

make %{makeprocesses}

%install
cd build
make install

%post
%{relocateConfig}GBLConfig.cmake
