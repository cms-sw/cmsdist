### RPM external gbl V04-00-07
## INCLUDE cpp-standard
## INCLUDE microarch_flags
Source: https://gitlab.desy.de/millepede/general-broken-lines/-/archive/%{realversion}/general-broken-lines-%{realversion}.tar.gz
Source99: scram-tools.file/tools/eigen/env

BuildRequires: cmake
Requires: eigen
Requires: mille

%prep
%setup -q -n general-broken-lines-%{realversion}

%build
rm -rf build
mkdir build
cd build
source %{_sourcedir}/env

cmake ../cpp \
  -DCMAKE_INSTALL_PREFIX=%{i} \
  -DCMAKE_BUILD_TYPE=%{cmake_build_type} \
  -DCMAKE_VERBOSE_MAKEFILE=ON \
  -DEIGEN3_INCLUDE_DIR=${EIGEN_ROOT}/include/eigen3 \
  -DCMAKE_PREFIX_PATH="%{cmake_prefix_path}" \
  -DCMAKE_CXX_COMPILER="g++" \
  -DCMAKE_CXX_FLAGS="$CMS_EIGEN_CXX_FLAGS %{selected_microarch}"

make %{makeprocesses} VERBOSE=1

%install
cd build
make install VERBOSE=1

%post
%{relocateConfig}GBLConfig.cmake
