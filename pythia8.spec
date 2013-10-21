### RPM external pythia8 153 

Requires: hepmc

Source: http://cern.ch/service-spi/external/MCGenerators/distribution/%{n}/%{n}-%{realversion}-src.tgz
Patch0: pythia8-patchhook

%if "%{?cms_cxxflags:set}" != "set"
%define cms_cxxflags -std=c++0x
%endif

%prep
%setup -q -n %{n}/%{realversion}
%patch0 -p1

export USRCXXFLAGS="%cms_cxxflags"
export HEPMCLOCATION=${HEPMC_ROOT} 
export HEPMCVERSION=${HEPMC_VERSION} 
./configure --enable-shared --with-hepmc=${HEPMC_ROOT}

%build
make 

%install
tar -c lib include xmldoc | tar -x -C %i
