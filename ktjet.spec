### RPM external ktjet 1.06
Requires: gcc-wrapper
Source: http://hepforge.cedar.ac.uk/hf/archive/ktjet/KtJet-%{v}.tar.gz
Requires: clhep
%prep
%setup -n KtJet-%{v}
%build
## IMPORT gcc-wrapper
CPPFLAGS=" -DKTDOUBLEPRECISION -fPIC" ./configure --with-clhep=$CLHEP_ROOT --prefix=%{i}
make
%install
make install
