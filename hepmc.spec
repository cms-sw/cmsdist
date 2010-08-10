### RPM external hepmc 2.05.01
Source: http://lcgapp.cern.ch/project/simu/HepMC/download/HepMC-%realversion.tar.gz
Patch0: hepmc-2.03.06-reflex

%prep
%setup -q -n HepMC-%{realversion}
%patch0 -p0

./configure --prefix=%{i} --with-momentum=GEV --with-length=MM F77="gfortran"

%build
make 

%install
make install
