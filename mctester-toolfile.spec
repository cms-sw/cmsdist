### RPM external mctester-toolfile 1.0
Requires: mctester
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/mctester.xml
<tool name="mctester" version="@TOOL_VERSION@">
  <lib name="HEPEvent"/>
  <lib name="HepMCEvent"/>
  <lib name="MCTester"/>
  <client>
    <environment name="MCTESTER_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$MCTESTER_BASE/lib"/>
    <environment name="INCLUDE" default="$MCTESTER_BASE/include"/>
  </client>
  <runtime name="MCTESTERLOCATION" value="$MCTESTER_BASE/lib/"/>
  <use name="root"/>
  <use name="HepMC"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post

