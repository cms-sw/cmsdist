### RPM lcg roofit-toolfile 1.0
Requires: roofit
%prep

%build

%install

mkdir -p %i/etc/scram.d

# roofitcore toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/roofitcore.xml
<tool name="roofitcore" version="@TOOL_VERSION@">
  <info url="http://root.cern.ch/root/"/>
  <lib name="RooFitCore"/>
  <client>
    <environment name="ROOFIT_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$ROOFIT_BASE/lib"/>
    <environment name="INCLUDE" default="$ROOFIT_BASE/include"/>
  </client>
  <runtime name="ROOFITSYS" value="$ROOFIT_BASE/"/>
  <runtime name="PATH"      value="$ROOFIT_BASE/bin" type="path"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$INCLUDE" type="path"/>
  <use name="rootcore"/>
  <use name="roothistmatrix"/>
  <use name="rootgpad"/>
  <use name="rootminuit"/>
  <use name="root_cxxdefaults"/>
</tool>
EOF_TOOLFILE

# roofit toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/roofit.xml
<tool name="roofit" version="@TOOL_VERSION@">
  <info url="http://root.cern.ch/root/"/>
  <lib name="RooFit"/>
  <use name="roofitcore"/>
  <use name="rootcore"/>
  <use name="rootmath"/>
  <use name="roothistmatrix"/>
</tool>
EOF_TOOLFILE

# roostats toolfile
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

# histfactory toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/histfactory.xml
<tool name="histfactory" version="@TOOL_VERSION@">
  <info url="http://root.cern.ch/root/"/>
  <lib name="HistFactory"/>
  <use name="roofitcore"/>
  <use name="roofit"/>
  <use name="roostats"/>
  <use name="rootcore"/>
  <use name="roothistmatrix"/>
  <use name="rootgpad"/>
  <use name="rootxml"/>
  <use name="rootfoam"/>
</tool>
EOF_TOOLFILE


## IMPORT scram-tools-post
