### RPM external photospp-toolfile 3.56
Requires: photospp
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/photosapp.xml
<tool name="photospp" version="@TOOL_VERSION@">
  <lib name="PhotosFortran"/>
  <lib name="PhotosCxxInterface"/>
  <client>
    <environment name="PHOTOSPP_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$PHOTOSPP_BASE/lib"/>
    <environment name="INCLUDE" default="$PHOTOSPP_BASE/include"/>
  </client>
  <use name="hepmc"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
