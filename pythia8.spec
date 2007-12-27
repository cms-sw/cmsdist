### RPM external pythia8 070-CMS19
Requires: hepmc
Requires: clhep
Requires: pythia6
Source: http://cern.ch/service-spi/external/MCGenerators/distribution/%{n}-%{realversion}-src.tgz
%prep
%setup -q -n %{n}/%{realversion}

export PYTHIA6LOCATION=${PYTHIA6_ROOT} 
export PYTHIA6VERSION=${PYTHIA6_VERSION} 
export HEPMCLOCATION=${HEPMC_ROOT} 
export HEPMCVERSION=${HEPMC_VERSION} 
export CLHEPLOCATION=${CLHEP_ROOT} 
export CLHEPVERSION=${CLHEP_VERSION}
./configure

%build
make 

%install
tar -c lib include | tar -x -C %i

# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=pythia8 version=%v>
<Client>
 <Environment name=PYTHIA8_BASE default="%i"></Environment>
 <Environment name=LIBDIR default="$PYTHIA8_BASE/lib"></Environment>
 <Environment name=INCLUDE default="$PYTHIA8_BASE/include"></Environment>
</Client>
<lib name=pythia8>
<use name=cxxcompiler>
<use name=hepmc>
<use name=pythia6>
<use name=clhep>
</Tool>
EOF_TOOLFILE

%post
%{relocateConfig}etc/scram.d/%n
