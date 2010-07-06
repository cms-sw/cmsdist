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
# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n.xml
  <tool name="%n" version="%v">
    <info url="http://www.ippp.dur.ac.uk/montecarlo/leshouches/generators/charybdis/"/>
    <lib name="charybdis"/>
    <client>
      <environment name="CHARYBDIS_BASE" default="%i"/>
      <environment name="LIBDIR" default="$CHARYBDIS_BASE/lib"/>
      <environment name="INCLUDE" default="$CHARYBDIS_BASE/include"/>
    </client>
    <use name="f77compiler"/>
    <use name="herwig"/>
    <use name="pythia6"/>
  </tool>
EOF_TOOLFILE

%post
%{relocateConfig}etc/scram.d/%n.xml
