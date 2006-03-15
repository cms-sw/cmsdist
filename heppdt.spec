### RPM external heppdt 2.02.02
Source: http://lcgapp.cern.ch/project/simu/HepPDT/download/HepPDT-%v.tar.gz
Requires: clhep
%prep
%setup -n HepPDT-%v
%build
mkdir -p objs
cd objs
../configure --prefix=%{i}
make -e CLHEP_DIR=$CLHEP_ROOT
%install
cd objs
make install
