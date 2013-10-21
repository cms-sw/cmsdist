### RPM external pythia8-175 175

Requires: hepmc

Source: http://cern.ch/service-spi/external/MCGenerators/distribution/pythia8/pythia8-%{realversion}-src.tgz
%prep
%setup -q -n pythia8/%{realversion}

export HEPMCLOCATION=${HEPMC_ROOT} 
export HEPMCVERSION=${HEPMC_VERSION} 
./configure --enable-shared --with-hepmc=${HEPMC_ROOT}

%build
make 

%install
tar -c lib include xmldoc | tar -x -C %i
