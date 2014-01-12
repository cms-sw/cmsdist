### RPM external yoda 1.0.4

Source: http://cern.ch/service-spi/external/MCGenerators/distribution/%{n}/%{n}-%{realversion}-src.tgz

Requires: boost python cython
Patch0: yoda-1.0.4-fixisnan

%if "%{?cms_cxxflags:set}" != "set"
%define cms_cxxflags -std=c++0x -O2
%endif

%prep
%setup -q -n %{n}/%{realversion}
%patch0 -p2

configure --prefix=%i --with-boost=${BOOST_ROOT} CXX="$(which %cms_cxx)" CXXFLAGS="%cms_cxxflags"

%build
make all

%install
make install
