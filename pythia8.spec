### RPM external pythia8 185

Requires: hepmc

Source: http://cern.ch/service-spi/external/MCGenerators/distribution/%{n}/%{n}-%{realversion}-src.tgz

%prep
%setup -q -n %{n}/%{realversion}

export HEPMCLOCATION=${HEPMC_ROOT} 
export HEPMCVERSION=${HEPMC_VERSION} 
./configure --prefix=%i --enable-shared --with-hepmc=${HEPMC_ROOT}

%build
make 

%install
make install
