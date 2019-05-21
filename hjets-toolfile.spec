### RPM external hjets-toolfile 1.0
Requires: hjets
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/vbfnlo.xml
<tool name="hjets" version="@TOOL_VERSION@">
  <lib name="hjets"/>
  <client>
    <environment name="HJETS_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$HJETS_BASE/lib/"/>
    <environment name="INCLUDE" default="$HJETS_BASE/include"/>
    <environment name="BINDIR" default="$HJETS_BASE/bin"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$INCLUDE" type="path"/>
  <runtime name="PATH" default="$BINDIR" type="path"/>
  <use name="herwigpp"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post

