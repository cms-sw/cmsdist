### RPM external yamlcpp 0.3.0

Source: http://cern.ch/service-spi/external/MCGenerators/distribution/%{n}/%{n}-%{realversion}-src.tgz

BuildRequires: cmake

Requires: boost

%if "%{?cms_cxxflags:set}" != "set"
%define cms_cxxflags -std=c++0x -O2
%endif

%prep
%setup -q -n %{n}/%{realversion}

cmake -DBOOST_ROOT=${BOOST_ROOT} -DCMAKE_INSTALL_PREFIX=%i -DBUILD_SHARED_LIBS=ON -DCMAKE_CXX_FLAGS="%{cms_cxxflags}"

%build
make 

%install
make install
