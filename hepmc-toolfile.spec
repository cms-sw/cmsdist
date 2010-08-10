### RPM external hepmc-toolfile 1.0
Requires: hepmc
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/hepmc.xml
<tool name="HepMC" version="@TOOL_VERSION@">
  <lib name="HepMCfio"/>
  <lib name="HepMC"/>
  <client>
    <environment name="HEPMC_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$HEPMC_BASE/lib"/>
    <environment name="INCLUDE" default="$HEPMC_BASE/include"/>
  </client>
  <runtime name="CMSSW_FWLITE_INCLUDE_PATH" value="$HEPMC_BASE/include" type="path"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
