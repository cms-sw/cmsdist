### RPM external herwig 6.510-cms2
Requires: gcc-wrapper
%define gccwrapperarch slc4_ia32_gcc345
%define realversion %(echo %v | cut -d- -f1)
Source: http://cern.ch/service-spi/external/MCGenerators/distribution/%{n}-%{realversion}-src.tgz
%prep
%setup -q -n %n
# Danger - herwig doesn't actually need the hepmc, clhep,lhapdf 
# that appear to be used in the configure
./configure 

%build
## IMPORT gcc-wrapper
make 

%install
tar -c lib include | tar -x -C %i

