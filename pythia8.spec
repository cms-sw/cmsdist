### RPM external pythia8 200pre2

Requires: hepmc lhapdf

#Source: http://cern.ch/service-spi/external/MCGenerators/distribution/%{n}/%{n}-%{realversion}-src.tgz
Source: https://cms-project-generators.web.cern.ch/cms-project-generators/%{n}-%{realversion}-src.tgz

%prep
%setup -q -n %{n}/%{realversion}

export HEPMCLOCATION=${HEPMC_ROOT}  
export HEPMCVERSION=${HEPMC_VERSION}
./configure --prefix=%i --enable-shared --with-hepmc2=${HEPMC_ROOT} --with-lhapdf5=${LHAPDF_ROOT}

%build
make 

%install
make install
