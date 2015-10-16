### RPM external yoda 1.5.5

Source: http://cern.ch/service-spi/external/MCGenerators/distribution/%{n}/%{n}-%{realversion}-src.tgz

Requires: boost python cython

%if "%{?cms_cxxflags:set}" != "set"
%define cms_cxxflags -std=c++0x -O2
%endif

%prep
%setup -q -n %{n}/%{realversion}

./configure --prefix=%i --with-boost=${BOOST_ROOT} CXX="$(which %cms_cxx)" CXXFLAGS="%cms_cxxflags"

%build
make all

%install
make install

%post
%{relocateConfig}bin/yoda-config
