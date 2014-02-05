### RPM external fastjet-contrib r543
Source:  svn://fastjet.hepforge.org/svn/contrib/trunk?scheme=http&module=fjcontrib&revision=543&output=/fjcontrib-%realversion.tar.gz
Requires: fastjet
%define keep_archives true

%prep
%setup -n fjcontrib
./configure --prefix=%i --fastjet-config=$FASTJET_ROOT/bin/fastjet-config CXXFLAGS="-I$FASTJET_ROOT/include"

%build
scripts/update-contribs.sh
make
make check

%install
mkdir -p %i/lib
mkdir ${FASTJET_ROOT}/include/fastjet/contrib
cp `find . -name "*.hh"` ${FASTJET_ROOT}/include/fastjet/contrib
make install
make fragile-shared
make fragile-shared-install
