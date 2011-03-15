### RPM external tauolapp 1.0.2a
Source: http://cern.ch/service-spi/external/MCGenerators/distribution/tauola++-%{realversion}-src.tgz
Requires: hepmc

%prep
%setup -q -n tauola++/%{realversion}
./configure --prefix=%{i} --with-HepMC=$HEPMC_ROOT

%build
make

%install
make install
