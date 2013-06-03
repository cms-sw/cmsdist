### RPM external heppid 0.02.01
Source: http://cepa.fnal.gov/dist/hep/HepPID-%v-src.tar.gz
%prep
%setup -n HepPID
%build
mkdir -p objs
cd objs
../configure --prefix=%{i}
make %makeprocesses
%install
cd objs
make install
