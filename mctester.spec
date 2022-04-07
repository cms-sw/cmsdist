### RPM external mctester 1.25.1

Source: https://gitlab.cern.ch/cvsmctst/mc-tester/-/archive/v%{realversion}/mc-tester-v%{realversion}.tar.gz

Requires: hepmc
Requires: root

BuildRequires: autotools

%define keep_archives true


%prep
%setup -q -n mc-tester-v%{realversion}

./configure \
  --with-HepMC=${HEPMC_ROOT} \
  --with-root=${ROOT_ROOT} \
  --prefix=%i

%build
make

%install
make install

%ifarch darwin
find %i/lib -name "*.dylib" -exec install_name_tool -change '../lib/libHEPEvent.dylib' 'libHEPEvent.dylib' {} \;
%endif
