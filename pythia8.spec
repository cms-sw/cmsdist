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

export PYTHIA6LOCATION=${PYTHIA6_ROOT} 
export PYTHIA6VERSION=${PYTHIA6_VERSION} 
export HEPMCLOCATION=${HEPMC_ROOT} 
export HEPMCVERSION=${HEPMC_VERSION} 
export CLHEPLOCATION=${CLHEP_ROOT} 
export CLHEPVERSION=${CLHEP_VERSION}
./configure

%build
%if "%{cmsplatf}" == "%{gccwrapperarch}"
echo "Using gcc wrapper for %cmsplatf"
source $GCC_WRAPPER_ROOT/etc/profile.d/init.sh
%endif
make 

%install
tar -c lib include | tar -x -C %i

