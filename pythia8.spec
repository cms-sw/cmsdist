### RPM external pythia8 180

Requires: hepmc

Source: http://cern.ch/service-spi/external/MCGenerators/distribution/%{n}/%{n}-%{realversion}-src.tgz

%if "%{?cms_cxxflags:set}" != "set"
%define cms_cxxflags -std=c++0x
%endif

%prep
%setup -q -n %{n}/%{realversion}

export USRCXXFLAGS="%cms_cxxflags"
./configure --prefix=%i --enable-shared --with-hepmc=${HEPMC_ROOT}

%build
make 

%install
make install
