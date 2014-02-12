### RPM external fastjet-contrib 1.008
Source: http://fastjet.hepforge.org/contrib/downloads/fjcontrib-%realversion.tar.gz
Requires: fastjet
%define keep_archives true

%prep
%setup -n fjcontrib-%realversion
./configure --prefix=%i --fastjet-config=$FASTJET_ROOT/bin/fastjet-config CXXFLAGS="-fPIC -I$FASTJET_ROOT/include"

%build
make
make check

%install
make install
