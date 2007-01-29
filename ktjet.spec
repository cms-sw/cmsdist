### RPM external ktjet 1.07
Source: http://hepforge.cedar.ac.uk/hf/archive/ktjet/KtJet-1.07.tar.gz
Requires: clhep
%prep
%setup -n KtJet-1.07
%build
CPPFLAGS=" -DKTDOUBLEPRECISION" ./configure --with-clhep=$CLHEP_ROOT --prefix=%{i}
make
%install
make install
