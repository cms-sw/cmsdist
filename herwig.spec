### RPM external herwig 6.510-cms2
%define realversion %(echo %v | cut -d- -f1)
Source: http://cern.ch/service-spi/external/MCGenerators/distribution/%{n}-%{realversion}-src.tgz
%prep
%setup -q -n %n
# Danger - herwig doesn't actually need the hepmc, clhep,lhapdf 
# that appear to be used in the configure
./configure 

%build
make 

# then hack include area as jimmy depends on missing header file..
cd include
ln -sf HERWIG65.INC herwig65.inc

%install
tar -c lib include | tar -x -C %i

