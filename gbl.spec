### RPM external gbl V03-01-01
## INCLUDE cpp-standard
%define tag 59c2d99ea96bc739321fd251096504c91467be24
Source: git+https://gitlab.desy.de/claus.kleinwort/general-broken-lines.git?obj=main/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz

BuildRequires: cmake
Requires: eigen

%prep
%setup -q -n %{n}-%{realversion}

%build
rm -rf build
mkdir build
cd build

cmake ../cpp \
  -DCMAKE_INSTALL_PREFIX=%{i} \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_VERBOSE_MAKEFILE=ON \
  -DEIGEN3_INCLUDE_DIR=${EIGEN_ROOT}/include/eigen3 \
  -DSUPPORT_ROOT=False \
  %ifarch x86_64
  -DCMAKE_CXX_FLAGS="-DEIGEN_MAX_ALIGN_BYTES=64 -msse3" \
  %else
  -DCMAKE_CXX_FLAGS="-DEIGEN_MAX_ALIGN_BYTES=64" \
  %endif
  -DCMAKE_CXX_STANDARD=%{cms_cxx_standard}

make %{makeprocesses}

%install
cd build
make install

%post
%{relocateConfig}GBLConfig.cmake
