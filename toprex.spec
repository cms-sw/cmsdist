### RPM external toprex 4.23
## BUILDIF case $(uname):$(uname -p) in Linux:i*86 ) true ;; Linux:x86_64 ) true ;;  Linux:ppc64 ) false ;; Darwin:* ) false ;; * ) false ;; esac 

Source: http://cern.ch/service-spi/external/MCGenerators/distribution/%{n}-%{realversion}-src.tgz
Patch: toprex-4.23-gfortran

%prep
%setup -q -n %{n}/%{realversion}
case %gccver in
  4.*)
%patch -p0 
  ;; 
esac

%build
./configure --lcgplatform=%cmsplatf
make 

%install
tar -c lib include | tar -x -C %i
