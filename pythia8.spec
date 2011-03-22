### RPM external pythia8 145

Requires: hepmc
Requires: clhep
Requires: pythia6
Requires: lhapdf

Source: http://cern.ch/service-spi/external/MCGenerators/distribution/%{n}-%{realversion}-src.tgz
%prep
%setup -q -n %{n}/%{realversion}

case %cmsplatf in
  slc*) ;;
  osx*_*_gcc*)
    export USRLDFLAGSSHARED="-Wl,-commons,use_dylibs"
  ;;
  *)
    echo "Make sure you handle commons!" ; exit 1 ;;
esac

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
