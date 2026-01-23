### RPM external gbl test-04-00-00 
## INCLUDE cpp-standard
## INCLUDE microarch_flags
%define tag 557a04237f121f5d444f7d8b69882d75b00ad5cb
Source: git+https://gitlab.desy.de/millepede/general-broken-lines.git?obj=main/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz
Source99: scram-tools.file/tools/eigen/env

BuildRequires: cmake
Requires: eigen
Requires: mille

%prep
%setup -q -n %{n}-%{realversion}
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
  -DCMAKE_CXX_FLAGS="$CMS_EIGEN_CXX_FLAGS %{selected_microarch}"

make %{makeprocesses}

%install
cd build
make install

%post
%{relocateConfig}GBLConfig.cmake
