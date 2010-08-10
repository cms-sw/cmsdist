### RPM external herwig 6.510.3
Source: http://cern.ch/service-spi/external/MCGenerators/distribution/%{n}-%{realversion}-src.tgz
Requires: lhapdf photos tauola
Patch1: herwig-6.510-tauola
Patch2: herwig-6.510.3-nmxhep

%prep
%setup -q -n %n/%{realversion}
# Danger - herwig doesn't actually need the hepmc, clhep,lhapdf 
# that appear to be used in the configure

# move tauola/photos dummy functions in new directory
mkdir tauoladummy
mv ./dummy/dexay.f ./tauoladummy/ 
mv ./dummy/inietc.f ./tauoladummy/ 
mv ./dummy/inimas.f ./tauoladummy/ 
mv ./dummy/iniphx.f ./tauoladummy/ 
mv ./dummy/initdk.f ./tauoladummy/ 
mv ./dummy/phoini.f ./tauoladummy/ 
mv ./dummy/photos.f ./tauoladummy/ 

# apply patch to modify Makefile
%patch1 -p2
%patch2 -p2

./configure --enable-shared

%build
make 

# then hack include area as jimmy depends on missing header file..
cd include
ln -sf HERWIG65.INC herwig65.inc

%install
tar -c lib include | tar -x -C %i
