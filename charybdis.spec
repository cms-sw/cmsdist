### RPM external charybdis 1.003
## BUILDIF case $(uname):$(uname -m) in Linux:i*86 ) true ;; Linux:x86_64 ) true ;;  Linux:ppc64 ) false ;; Darwin:* ) false ;; * ) false ;; esac 
Source: http://cern.ch/service-spi/external/MCGenerators/distribution/%{n}-%{realversion}-src.tgz
%prep
%setup -q -n %{n}/%{realversion}
./configure --lcgplatform=%cmsplatf --pythia_hadronization

%build
which g77
make

%install
tar -c lib include | tar -x -C %i
