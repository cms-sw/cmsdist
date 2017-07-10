### RPM external pythia8 226

Requires: hepmc lhapdf

Source: http://home.thep.lu.se/~torbjorn/pythia8/%{n}%{realversion}.tgz

%if "%{?cms_cxxflags:set}" != "set"
%define cms_cxxflags -std=c++0x
%endif

%prep
%setup -q -n %{n}%{realversion}

export USRCXXFLAGS="%cms_cxxflags"
./configure --prefix=%i --enable-shared --with-hepmc2=${HEPMC_ROOT} --with-lhapdf5=${LHAPDF_ROOT}

%build
make %makeprocesses

%install
make install
test -f %i/lib/libpythia8lhapdf5.so || exit 1
