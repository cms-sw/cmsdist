### RPM external herwig 6.510-cms2
Requires: gcc-wrapper
Requires: clhep
Requires: hepmc
Requires: lhapdf
%define gccwrapperarch slc4_ia32_gcc345
%define realversion %(echo %v | cut -d- -f1)
Source: http://cern.ch/service-spi/external/MCGenerators/distribution/%{n}-%{realversion}-src.tgz
%prep
%setup -q -n %n
./configure --with-hepmc=$HEPMC_BASE --with-clhep=$CLHEP_BASE --with-lhapdf=$LHAPDF_BASE 

%build
## IMPORT gcc-wrapper
make 

%install
tar -c lib include | tar -x -C %i

