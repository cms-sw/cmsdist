### RPM external photospp-toolfile 4.0
Requires: photospp
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/photospp.xml
<tool name="photospp" version="@TOOL_VERSION@">
  <lib name="Photospp"/>
  <lib name="PhotosppHepMC"/>
  <lib name="PhotosppHEPEVT"/>
  <client>
    <environment name="PHOTOSPP_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$PHOTOSPP_BASE/lib"/>
    <environment name="INCLUDE" default="$PHOTOSPP_BASE/include"/>
  </client>
  <use name="hepmc"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
# bla bla
