### RPM external evtgenlhc 8.16
Source: http://cern.ch/service-spi/external/MCGenerators/distribution/%{n}-%{realversion}-src.tgz
Requires: clhep

%prep
%setup -q -n %{n}/%{realversion}
./configure --lcgplatform=%cmsplatf --with-clhep=$CLHEP_ROOT

%build
make

%install
tar -c lib EvtGen EvtGenBase EvtGenModels DecFiles | tar -x -C %i
# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=evtgenlhc version=%v>
<Client>
 <Environment name=EVTGENLHC_BASE default="%i"></Environment>
 <Environment name=LIBDIR default="$EVTGENLHC_BASE/lib"></Environment>
 <Environment name=INCLUDE default="$EVTGENLHC_BASE"></Environment>
</Client>
<lib name=evtgenlhc>
<use name=clhep>
</Tool>
EOF_TOOLFILE

%post
%{relocateConfig}etc/scram.d/%n
