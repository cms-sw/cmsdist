### RPM external pythia8 226

Requires: hepmc lhapdf

Source: http://home.thep.lu.se/~torbjorn/pythia8/%{n}%{realversion}.tgz


%prep
%setup -q -n %{n}%{realversion}

./configure --prefix=%i --enable-shared --with-hepmc2=${HEPMC_ROOT} --with-lhapdf6=${LHAPDF_ROOT} --with-lhapdf6-plugin=LHAPDF6.h

%build
make %makeprocesses

%install
make install
test -f %i/lib/libpythia8lhapdf6.so || exit 1
