### RPM external hepmc 2.06.10

%define tag 307d0fb0853812142f3e47f85353ba3cf95bde28
%define branch dl210312_3
Source: git+https://github.com/davidlange6/hepmc.git?obj=%{branch}/%{tag}&export=HepMC-%{realversion}&output=/HepMC-%{realversion}.tgz

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
rm -rf %i/lib/*.la
