### RPM external hepmc 2.01.08
Requires: clhep
Source: http://lcgapp.cern.ch/project/simu/HepMC/download/HepMC-%realversion.tar.gz

%prep
%setup -q -n HepMC-%{realversion}

echo "CLHEP_ROOT is: " $CLHEP_ROOT
./configure  --with-CLHEP=$CLHEP_ROOT --prefix=%{i} 

%build
make 

%install
make install

# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=HepMC version=%v>
<lib name=HepMCfio>
<lib name=HepMC>
<Client>
 <Environment name=HEPMC_BASE default="%i"></Environment>
 <Environment name=LIBDIR default="$HEPMC_BASE/lib"></Environment>
 <Environment name=INCLUDE default="$HEPMC_BASE/include"></Environment>
</Client>
<use name=CLHEP>
</Tool>
EOF_TOOLFILE

%post
%{relocateConfig}etc/scram.d/%n
