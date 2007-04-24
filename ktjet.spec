### RPM external ktjet 1.06
Source: http://hepforge.cedar.ac.uk/hf/archive/ktjet/KtJet-%{v}.tar.gz
Requires: clhep
%prep
%setup -n KtJet-%{v}
%build
CPPFLAGS=" -DKTDOUBLEPRECISION" ./configure --with-clhep=$CLHEP_ROOT --prefix=%{i}
make
%install
make install
