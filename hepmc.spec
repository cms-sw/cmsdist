### RPM external hepmc 2.06.10

%define tag 91c4c217572ac25669e9ad8fdc0111d1d5c82289
%define branch cms/%{realversion}
Source: git+https://github.com/cms-externals/hepmc.git?obj=%{branch}/%{tag}&export=HepMC-%{realversion}&output=/HepMC-%{realversion}.tgz

BuildRequires: cmake

%define keep_archives true
%define drop_files %i/share

%prep
%setup -q -n HepMC-%{realversion}

%build

rm -rf ../build
mkdir ../build
cd ../build

cmake ../HepMC-%{realversion} \
    -DCMAKE_INSTALL_PREFIX=%{i} \
    -DCMAKE_CXX_FLAGS="-fPIC" \
    -DCMAKE_BUILD_TYPE="Release" \
    -Dmomentum:STRING=GEV \
    -Dlength:STRING=MM 

make %makeprocesses

%install
cd ../build
make install
rm -rf %i/lib/*.so
rm -rf %i/lib/*.la
