### RPM external ktjet 1.06-CMS4
Source: http://hepforge.cedar.ac.uk/hf/archive/ktjet/KtJet-%{realversion}.tar.gz
Patch1: ktjet-1.0.6-nobanner
Requires: clhep

%prep
%setup -n KtJet-%{realversion}
%patch1 -p1

%build
CPPFLAGS=" -DKTDOUBLEPRECISION -fPIC" ./configure --with-clhep=$CLHEP_ROOT --prefix=%{i}
make
%install
make install
