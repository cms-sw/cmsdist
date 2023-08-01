### RPM external gbl V02-04-01

%define tag 31e726d777fe93cdbed0c363dc15f803f7767f40
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
  -DEIGEN3_INCLUDE_DIR=${EIGEN_ROOT}/include/eigen3 \
  -DSUPPORT_ROOT=False \
  -DCMAKE_CXX_STANDARD=17

make %{makeprocesses}

%install
cd build
make install

%post
%{relocateConfig}GBLConfig.cmake
