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
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n
<doc type="BuildSystem::ToolDoc" version="1.0">
<Tool name="charybdis" version="%v">
<info url="http://www.ippp.dur.ac.uk/montecarlo/leshouches/generators/charybdis/"/>
<Client>
 <Environment name="CHARYBDIS_BASE" default="%i"></Environment>
 <Environment name="LIBDIR" default="$CHARYBDIS_BASE/lib"></Environment>
 <Environment name="INCLUDE" default="$CHARYBDIS_BASE/include"></Environment>
</Client>
<lib name="charybdis"/>
<use name="f77compiler"/>
<use name="herwig"/>
<use name="pythia6"/>
</Tool>
</doc>
EOF_TOOLFILE

%post
%{relocateConfig}etc/scram.d/%n
