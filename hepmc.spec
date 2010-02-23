### RPM external hepmc 2.05.01
Source: http://lcgapp.cern.ch/project/simu/HepMC/download/HepMC-%realversion.tar.gz

%prep
%setup -q -n HepMC-%{realversion}

./configure --prefix=%{i} --with-momentum=GEV --with-length=MM F77="gfortran"

%build
make 

%install
make install

# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n.xml
  <tool name="HepMC" version="%v">
    <lib name="HepMCfio"/>
    <lib name="HepMC"/>
    <client>
      <environment name="HEPMC_BASE" default="%i"/>
      <environment name="LIBDIR" default="$HEPMC_BASE/lib"/>
      <environment name="INCLUDE" default="$HEPMC_BASE/include"/>
    </client>
    <runtime name="CMSSW_FWLITE_INCLUDE_PATH" value="$HEPMC_BASE/include" type="path"/>
  </tool>
EOF_TOOLFILE

%post
%{relocateConfig}etc/scram.d/%n.xml
