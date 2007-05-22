### RPM external ktjet 1.06-XXXX
Source: http://hepforge.cedar.ac.uk/hf/archive/ktjet/KtJet-%{realversion}.tar.gz
Requires: clhep
%prep
%setup -n KtJet-%{realversion}
%build
CPPFLAGS=" -DKTDOUBLEPRECISION -fPIC" ./configure --with-clhep=$CLHEP_ROOT --prefix=%{i}
make
%install
make install
