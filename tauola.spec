### RPM external tauola 27.121.5
## BUILDIF case $(uname):$(uname -p) in Linux:i*86 ) true ;; Linux:x86_64 ) true ;;  Linux:ppc64 ) false ;; Darwin:* ) false ;; * ) false ;; esac     
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
# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n.xml
  <tool name="tauola" version="%v">
    <lib name="tauola"/>
    <lib name="pretauola"/>
    <client>
      <environment name="TAUOLA_BASE" default="%i"/>
      <environment name="LIBDIR" default="$TAUOLA_BASE/lib"/>
      <environment name="INCLUDE" default="$TAUOLA_BASE/include"/>
    </client>
    <use name="f77compiler"/>
    <use name="pythia6"/>
  </tool>
EOF_TOOLFILE

%post
%{relocateConfig}etc/scram.d/%n.xml
