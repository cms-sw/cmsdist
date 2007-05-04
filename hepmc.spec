### RPM external hepmc 2.00.02
Requires: gcc-wrapper
Requires: clhep
Source: http://lcgapp.cern.ch/project/simu/HepMC/download/HepMC-%v.tar.gz

%prep
%setup -q -n HepMC-%{v}

echo "CLHEP_ROOT is: " $CLHEP_ROOT
./configure  --with-CLHEP=$CLHEP_ROOT --prefix=%{i} 

%build
## IMPORT gcc-wrapper
make 

%install
make install
