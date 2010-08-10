### RPM external tauola 27.121.5
## BUILDIF case $(uname):$(uname -m) in Linux:i*86 ) true ;; Linux:x86_64 ) true ;;  Linux:ppc64 ) false ;; Darwin:* ) false ;; * ) false ;; esac     
Source: http://cern.ch/service-spi/external/MCGenerators/distribution/%{n}-%{realversion}-src.tgz
Patch: tauola-27.121-gfortran
Patch1: tauola-27.121.5-gfortran-taueta
Requires: pythia6

%prep
%setup -q -n %{n}/%{realversion}
case %gccver in
  4.*)
%patch -p0 
%patch1 -p2
  ;;
esac
./configure --lcgplatform=%cmsplatf --with-pythia6libs=$PYTHIA6_ROOT/lib

%build
make

%install
tar -c lib include | tar -x -C %i
