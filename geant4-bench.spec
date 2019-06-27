### RPM external geant4-bench 1.0.0

BuildRequires: geant4-parfullcms
BuildRequires: geant4data

%prep
# NOP

%build
# NOP

%install

mkdir -p %{i}
cd %{i}

# Copy required files
cp -r ${GEANT4_PARFULLCMS_ROOT}/share/ParFullCMS .

# Set number of threads
export G4FORCENUMBEROFTHREADS=max

# export GEANT4 data files
export G4LEDATA
export G4LEVELGAMMADATA
export G4SAIDXSDATA
export G4NEUTRONXSDATA

# Adjust event size
sed -ibak 's;\(/run/beamOn \).*;\1800;' ParFullCMS/mt.g4

# Launch bechmark
cd ParFullCMS
ParFullCMS mt.g4 2>&1 | tee run.log
# bla bla
