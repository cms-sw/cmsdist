### RPM external pythia8-toolfile 1.0
Requires: pythia8
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/pythia8.xml
<tool name="pythia8" version="@TOOL_VERSION@">
  <lib name="pythia8"/>
  <lib name="pythia8tohepmc"/>
  <client>
    <environment name="PYTHIA8_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$PYTHIA8_BASE/lib"/>
    <environment name="INCLUDE" default="$PYTHIA8_BASE/include"/>
  </client>
  <runtime name="PYTHIA8DATA" value="$PYTHIA8_BASE/xmldoc"/>
  <use name="hepmc"/>
  <use name="lhapdf"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
