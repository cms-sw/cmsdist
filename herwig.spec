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
# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n.xml
  <tool name="herwig" version="%v">
    <lib name="herwig"/>
    <lib name="herwig_dummy"/>
    <client>
      <environment name="HERWIG_BASE" default="%i"/>
      <environment name="LIBDIR" default="$HERWIG_BASE/lib"/>
      <environment name="INCLUDE" default="$HERWIG_BASE/include"/>
    </client>
    <use name="f77compiler"/>
    <use name="lhapdf"/>
    <use name="tauola"/>
    <use name="photos"/>
  </tool>
EOF_TOOLFILE

%post
%{relocateConfig}etc/scram.d/%n.xml
