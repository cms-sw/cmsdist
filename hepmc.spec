### RPM external hepmc 2.06.10
## INCLUDE cpp-standard

%define tag 97620c648f31c9129b42c0b38fe4bd1ddfee9cab
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
    -DCMAKE_CXX_STANDARD=%{cms_cxx_standard} \
    -Dmomentum:STRING=GEV \
    -Dlength:STRING=MM 

make %makeprocesses

%install
cd ../build
make install
rm -rf %i/lib/*.so
rm -rf %i/lib/*.la
