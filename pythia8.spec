### RPM external pythia8 310

Source: https://pythia.org/download/pythia83/%{n}%{realversion}.tgz
# https://gitlab.com/Pythia8/releases/-/issues/289: fix compilation of C++20 code with pythia8

Requires: hepmc hepmc3 lhapdf

%prep
%setup -q -n %{n}%{realversion}

./configure --prefix=%i --enable-shared --with-hepmc2=${HEPMC_ROOT} --with-hepmc3=${HEPMC3_ROOT} --with-lhapdf6=${LHAPDF_ROOT} --enable-mg5mes

%build
make %makeprocesses

%install
make install
test -f %i/lib/libpythia8lhapdf6.so || exit 1
rm -rf %{i}/share/Pythia8/examples

%post
%{relocateConfig}bin/pythia8-config
