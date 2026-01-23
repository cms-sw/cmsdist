### RPM external mille V00-01-02
## INCLUDE cpp-standard
Source: https://gitlab.desy.de/millepede/Mille/-/archive/%{realversion}/%{n}-%{realversion}.tar.gz
BuildRequires: cmake
Requires: zlib
Requires: root

%prep
%setup -n %{n}-%{realversion}

%build
rm -rf build
mkdir build
cd build
cmake \
  -DCMAKE_INSTALL_PREFIX=%{i} \
  ../
make 

%install
cd build
make install PREFIX=%{i}

%post
%{relocateConfig}cmake/MilleConfig.cmake
