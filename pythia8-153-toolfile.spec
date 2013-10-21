### RPM external pythia8-153-toolfile 1.0
Requires: pythia8-153
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/pythia8.xml
<tool name="pythia8-153" version="@TOOL_VERSION@">
  <lib name="pythia8_153"/>
  <lib name="hepmcinterface_153"/>
  <client>
    <environment name="PYTHIA8_153_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$PYTHIA8_153_BASE/lib"/>
    <environment name="INCLUDE" default="$PYTHIA8_153_BASE/include"/>
  </client>
  <runtime name="PYTHIA8153DATA" value="$PYTHIA8_153_BASE/xmldoc"/>
  <use name="hepmc"/>
  <use name="pythia6"/>
  <use name="clhep"/>
  <use name="lhapdf"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post

