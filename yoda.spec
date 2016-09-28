### RPM external yoda 1.6.4

Source: http://cern.ch/service-spi/external/MCGenerators/distribution/%{n}/%{n}-%{realversion}-src.tgz
#Source: http://www.hepforge.org/archive/yoda/YODA-%{realversion}.tar.gz

Requires: boost python cython
#Requires: python cython

%if "%{?cms_cxxflags:set}" != "set"
%define cms_cxxflags -std=c++0x -O2
%endif

%prep
%setup -q -n %{n}/%{realversion}
#%setup -q -n YODA-%{realversion}

./configure --prefix=%i --with-boost=${BOOST_ROOT} CXX="$(which %cms_cxx)" CXXFLAGS="%cms_cxxflags"

%build
make all

%install
make install

%post
%{relocateConfig}bin/yoda-config
