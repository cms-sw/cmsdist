### RPM external gbl V02-01-03

Source: svn://svnsrv.desy.de/public/GeneralBrokenLines/tags/%{realversion}/cpp/?scheme=http&module=%{realversion}&output=/%{n}-%{realversion}.tgz

BuildRequires: cmake
Requires: eigen

%prep
%setup -q -n %{realversion}

%build
rm -rf build
mkdir build
cd build

cmake .. \
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
# bla bla
