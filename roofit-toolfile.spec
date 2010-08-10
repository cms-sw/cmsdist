### RPM lcg roofit-toolfile 1.0
Requires: roofit
%prep

%build

%install

mkdir -p %i/etc/scram.d

# rootroofitcore toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/roofitcore.xml
<tool name="roofitcore" version="@TOOL_VERSION@">
  <info url="http://root.cern.ch/root/"/>
  <lib name="RooFitCore"/>
  <client>
    <environment name="ROOFIT_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$ROOFIT_BASE/lib"/>
    <environment name="INCLUDE" default="$ROOFIT_BASE/include"/>
  </client>
  <use name="rootcore"/>
  <use name="roothistmatrix"/>
  <use name="rootgpad"/>
  <use name="rootminuit"/>
</tool>
EOF_TOOLFILE

# rootroofit toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/roofit.xml
<tool name="roofit" version="@TOOL_VERSION@">
  <info url="http://root.cern.ch/root/"/>
  <lib name="RooFit"/>
  <use name="roofitcore"/>
  <use name="rootcore"/>
  <use name="roothistmatrix"/>
</tool>
EOF_TOOLFILE

# rootroostats toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/roostats.xml
<tool name="roostats" version="@TOOL_VERSION@">
  <info url="http://root.cern.ch/root/"/>
  <lib name="RooStats"/>
  <use name="roofitcore"/>
  <use name="roofit"/>
  <use name="rootcore"/>
  <use name="roothistmatrix"/>
  <use name="rootgpad"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
