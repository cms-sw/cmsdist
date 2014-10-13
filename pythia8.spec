### RPM external pythia8 200

Requires: hepmc lhapdf

Source: http://home.thep.lu.se/~torbjorn/pythia8/%{n}%{realversion}.tgz

Patch0: pythia8-200-fix-gcc-options

%prep
%setup -q -n %{n}%{realversion}

export HEPMCLOCATION=${HEPMC_ROOT}  
export HEPMCVERSION=${HEPMC_VERSION}
./configure --prefix=%i --enable-shared --with-hepmc2=${HEPMC_ROOT} --with-lhapdf5=${LHAPDF_ROOT}

%build
make 

%install
make install
