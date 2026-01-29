### RPM external mille V01-00-00
## INCLUDE cpp-standard
## INITENV +PATH PYTHON3PATH %{i}/python

Source: https://gitlab.desy.de/millepede/Mille/-/archive/%{realversion}/%{n}-%{realversion}.tar.gz
BuildRequires: cmake
Requires: zlib
Requires: root

%prep
%setup -n %{n}-%{realversion}

%build
rm -rf ../build
mkdir ../build
cd ../build
cmake \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_INSTALL_PREFIX=%{i} \
  -DCMAKE_PREFIX_PATH="%{cmake_prefix_path}" \
  -DCMAKE_CXX_STANDARD=%{cms_cxx_standard} \
  ../%{n}-%{realversion}
make  %{makeprocesses} VERBOSE=1
%install
cd ../build
make install PREFIX=%{i}

%post
%{relocateConfig}milleStandaloneSetup.sh
%{relocateConfig}cmake/MilleConfig.cmake
