### RPM external jimmy 4.2
## BUILDIF case $(uname):$(uname -m) in Linux:i*86 ) true ;; Linux:x86_64 ) true ;;  Linux:ppc64 ) false ;; Darwin:* ) false ;; * ) false ;; esac 

Requires: herwig
Source: http://service-spi.web.cern.ch/service-spi/external/MCGenerators/distribution/%{n}-%{realversion}-src.tgz
Patch: jimmy-4.2-gfortran

%prep
%setup -q -n %{n}/%{realversion}
case %gccver in
  4.*)
%patch -p0
  ;;
esac

%build
./configure --with-herwig=$HERWIG_ROOT
make 

%install
tar -c lib include | tar -x -C %i
