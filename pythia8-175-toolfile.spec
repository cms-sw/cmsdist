### RPM external pythia8-175-toolfile 1.0
Requires: pythia8-175
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/pythia8-175.xml
<tool name="pythia8-175" version="@TOOL_VERSION@">
  <lib name="pythia8"/>
  <lib name="hepmcinterface"/>
  <client>
    <environment name="PYTHIA8_175_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$PYTHIA8_175_BASE/lib"/>
    <environment name="INCLUDE" default="$PYTHIA8_175_BASE/include"/>
  </client>
  <runtime name="PYTHIA8175DATA" value="$PYTHIA8_175_BASE/xmldoc"/>
  <use name="hepmc"/>
  <use name="pythia6"/>
  <use name="clhep"/>
  <use name="lhapdf"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post

