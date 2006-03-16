### RPM external hepmc 1.26
Requires: clhep
Source: http://lcgapp.cern.ch/project/simu/HepMC/download/HepMC-%v.tar.gz

%prep
%setup -q -n HepMC-%{v}

echo "CLHEP_ROOT is: " $CLHEP_ROOT
./configure  --with-CLHEP=$CLHEP_ROOT --prefix=%{i} 

%build
make 

%install
make install
