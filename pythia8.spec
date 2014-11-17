### RPM external pythia8 201

Requires: hepmc lhapdf

Source: http://cern.ch/service-spi/external/MCGenerators/distribution/%{n}/%{n}-%{realversion}-src.tgz

Patch0: pythia8-201-fix-gcc-options
Patch1: pythia8-201-fix-init

%prep
%setup -q -n %{n}/%{realversion}
%patch0 -p2
%patch1 -p2

export HEPMCLOCATION=${HEPMC_ROOT}  
export HEPMCVERSION=${HEPMC_VERSION}
./configure --prefix=%i --enable-shared --with-hepmc2=${HEPMC_ROOT} --with-lhapdf5=${LHAPDF_ROOT}

%build
make 

%install
make install
