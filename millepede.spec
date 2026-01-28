### RPM external millepede V05-00-00 
## INCLUDE cpp-standard
Source: https://gitlab.desy.de/millepede/millepede-ii/-/archive/%{realversion}/%{n}-ii-%{realversion}.tar.gz
BuildRequires: cmake
Requires: root
Requires: mille

%prep
%setup -n %{n}-ii-%{realversion}

%build
rm -rf build
mkdir build
cd build
cmake \
  -DCMAKE_INSTALL_PREFIX=%{i} \
  -DLAPACK_OPENBLAS=off \
  ../
make 

%install
cd build
make install PREFIX=%{i}

%post
%{relocateConfig}cmake/millepedeIIConfig.cmake
