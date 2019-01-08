### RPM external pythia8 240

Source: http://home.thep.lu.se/~torbjorn/pythia8/%{n}%{realversion}.tgz

Requires: hepmc lhapdf

%prep
%setup -q -n %{n}%{realversion}

./configure --prefix=%i --enable-shared --with-hepmc2=${HEPMC_ROOT} --with-lhapdf6=${LHAPDF_ROOT}

%build
make %makeprocesses

%install
make install
test -f %i/lib/libpythia8lhapdf6.so || exit 1
