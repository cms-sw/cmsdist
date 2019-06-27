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
  </client>
  <use name="hepmc_headers"/>
  <runtime name="CMSSW_FWLITE_INCLUDE_PATH" value="$HEPMC_BASE/include" type="path"/>
</tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%i/etc/scram.d/hepmc_headers.xml
<tool name="hepmc_headers" version="@TOOL_VERSION@">
  <client>
    <environment name="HEPMC_HEADERS_BASE" default="@TOOL_ROOT@"/>
    <environment name="INCLUDE" default="$HEPMC_HEADERS_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH"  value="$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post

# bla bla
