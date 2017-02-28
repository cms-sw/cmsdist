### RPM external pythia8 223

Requires: hepmc lhapdf

Source: http://home.thep.lu.se/~torbjorn/pythia8/%{n}%{realversion}.tgz

Patch0: pythia8_223_diffractiveParameters

%if "%{?cms_cxxflags:set}" != "set"
%define cms_cxxflags -std=c++0x
%endif

%prep
%setup -q -n %{n}%{realversion}
%patch0 -p0

export USRCXXFLAGS="%cms_cxxflags"
./configure --prefix=%i --enable-shared --with-hepmc2=${HEPMC_ROOT} --with-lhapdf6=${LHAPDF_ROOT}

%build
make %makeprocesses

%install
make install
test -f %i/lib/libpythia8lhapdf6.so || exit 1
