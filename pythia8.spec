### RPM external pythia8 070
Requires: gcc-wrapper
Requires: hepmc
Requires: clhep
Requires: pythia6
%define gccwrapperarch slc4_ia32_gcc345
%define realversion %(echo %v | cut -d- -f1 )
Source: http://service-spi.web.cern.ch/service-spi/external/MCGenerators/distribution/%{n}-%{realversion}-src.tgz
%prep
%setup -q -n %{n}/%{realversion}
echo "./configure PYTHIA6LOCATION=${PYTHIA6_ROOT} PYTHIA6VERSION=${PYTHIA6_VERSION} HEPMCLOCATION=${HEPMC_ROOT} HEPMCVERSION=${HEPMC_VERSION} CLHEPLOCATION=${CLHEP_ROOT} CLHEPVERSION=${CLHEP_VERSION}"
./configure PYTHIA6LOCATION=${PYTHIA6_ROOT} PYTHIA6VERSION=${PYTHIA6_VERSION} HEPMCLOCATION=${HEPMC_ROOT} HEPMCVERSION=${HEPMC_VERSION} CLHEPLOCATION=${CLHEP_ROOT} CLHEPVERSION=${CLHEP_VERSION}

%build
%if "%{cmsplatf}" == "%{gccwrapperarch}"
echo "Using gcc wrapper for %cmsplatf"
source $GCC_WRAPPER_ROOT/etc/profile.d/init.sh
%endif
make 

%install
tar -c lib include | tar -x -C %i

