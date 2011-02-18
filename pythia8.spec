### RPM external pythia8 142

Requires: hepmc
Requires: clhep
Requires: pythia6
Requires: lhapdf

Source: http://cern.ch/service-spi/external/MCGenerators/distribution/%{n}-%{realversion}-src.tgz
%prep
%setup -q -n %{n}/%{realversion}

export PYTHIA6LOCATION=${PYTHIA6_ROOT} 
export PYTHIA6VERSION=${PYTHIA6_VERSION} 
export HEPMCLOCATION=${HEPMC_ROOT} 
export HEPMCVERSION=${HEPMC_VERSION} 
export CLHEPLOCATION=${CLHEP_ROOT} 
export CLHEPVERSION=${CLHEP_VERSION}
./configure --enable-shared --with-hepmc=${HEPMC_ROOT}

%build
make 

%install
tar -c lib include xmldoc | tar -x -C %i
