### RPM external ktjet 1.06
Source: http://www.hepforge.org/archive/ktjet/KtJet-%{realversion}.tar.gz
Patch1: ktjet-1.0.6-nobanner
Requires: clhep

%define keep_archives true

%prep
%setup -n KtJet-%{realversion}
%patch1 -p1

%build
CPPFLAGS=" -DKTDOUBLEPRECISION -fPIC" ./configure --with-clhep=$CLHEP_ROOT --prefix=%{i}
make
# bla bla
