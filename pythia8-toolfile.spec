### RPM external pythia8-toolfile 1.0
Requires: pythia8
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/pythia8.xml
<tool name="pythia8" version="@TOOL_VERSION@">
  <lib name="pythia8"/>
  <lib name="hepmcinterface"/>
  <client>
    <environment name="PYTHIA8_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$PYTHIA8_BASE/lib"/>
    <environment name="INCLUDE" default="$PYTHIA8_BASE/include"/>
  </client>
  <runtime name="PYTHIA8DATA" value="$PYTHIA8_BASE/xmldoc"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
  <use name="cxxcompiler"/>
  <use name="hepmc"/>
  <use name="pythia6"/>
  <use name="clhep"/>
  <use name="lhapdf"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post

