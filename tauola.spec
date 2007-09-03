### RPM external tauola 27.121-CMS8
Source: http://cern.ch/service-spi/external/MCGenerators/distribution/%{n}-%{realversion}-src.tgz
Requires: pythia6
%prep
%setup -q -n %{n}/%{realversion}
./configure --lcgplatform=%cmsplatf

%build
make 

%install
tar -c lib include | tar -x -C %i
# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=tauola version=%v>
<Client>
 <Environment name=TAUOLA_BASE default="%i"></Environment>
 <Environment name=LIBDIR default="$TAUOLA_BASE/lib"></Environment>
 <Environment name=INCLUDE default="$TAUOLA_BASE/include"></Environment>
</Client>
<lib name=tauola>
<lib name=pretauola>
<use name=f77compiler>
<use name=pythia6>
</Tool>
EOF_TOOLFILE

%post
%{relocateConfig}etc/scram.d/%n
