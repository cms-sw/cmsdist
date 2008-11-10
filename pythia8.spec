### RPM external pythia8 108
Requires: hepmc
Requires: clhep
Requires: pythia6
Requires: lhapdf

Source: http://cern.ch/service-spi/external/MCGenerators/distribution/%{n}-%{realversion}-src.tgz
%prep
%setup -q -n %{n}/%{realversion}

export PYTHIA6LOCATION=${PYTHIA6_ROOT} 
export PYTHIA6VERSION=${PYTHIA6_VERSION} 
export HEPMCLOCATION=${HEPMC_ROOT} 
export HEPMCVERSION=${HEPMC_VERSION} 
export CLHEPLOCATION=${CLHEP_ROOT} 
export CLHEPVERSION=${CLHEP_VERSION}
./configure --enable-shared --with-hepmc=${HEPMC_ROOT}

%build
make 

%install
tar -c lib include xmldoc | tar -x -C %i

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
<runtime name=PYTHIA8DATA value="$PYTHIA8_BASE/xmldoc">
<lib name=pythia8>
<lib name=hepmcinterface>
<use name=cxxcompiler>
<use name=hepmc>
<use name=pythia6>
<use name=clhep>
<use name=lhapdf>
</Tool>
EOF_TOOLFILE

%post
%{relocateConfig}etc/scram.d/%n
