### RPM external pythia8-153 153

Requires: hepmc

Source: http://cern.ch/service-spi/external/MCGenerators/distribution/pythia8/pythia8-%{realversion}-src.tgz
Patch0: pythia8-patchhook

%prep
%setup -q -n pythia8/%{realversion}
%patch0 -p1

export HEPMCLOCATION=${HEPMC_ROOT} 
export HEPMCVERSION=${HEPMC_VERSION} 
./configure --enable-shared --with-hepmc=${HEPMC_ROOT}

%build
make 

%install
tar -c lib include xmldoc | tar -x -C %i
