### RPM external gbl V03-01-00

%define tag 45bba8092133fefad57e82e7b91fb783075bb978
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
  -DSUPPORT_ROOT=False

make %{makeprocesses}

%install
cd build
make install

%post
%{relocateConfig}GBLConfig.cmake
