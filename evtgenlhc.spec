### RPM external evtgenlhc 9.1
## BUILDIF case $(uname):$(uname -m) in Linux:i*86 ) true ;; Linux:x86_64 ) true ;;  Linux:ppc64 ) false ;; Darwin:* ) false ;; * ) false ;; esac     

Source: http://cern.ch/service-spi/external/MCGenerators/distribution/%{n}-%{realversion}-src.tgz
Patch0: evtgenlhc-8.16-EvtPythia-iosfwd
Patch1: evtgenlhc-9.1-gcc43
Patch2: evtgenlhc-9.1-CLHEP2
Requires: clhep

%prep
%setup -q -n %{n}/%{realversion}
%patch0 -p2
%patch1 -p2
%patch2 -p2

%build
./configure --lcgplatform=%cmsplatf --with-clhep=$CLHEP_ROOT
make

%install
tar -c lib EvtGen EvtGenBase EvtGenModels DecFiles | tar -x -C %i
