### RPM external qgraf-toolfile 1.0
Requires: qgraf
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/qgraf.xml
<tool name="qgraf" version="@TOOL_VERSION@">
  <client>
    <environment name="QGRAF_BASE" default="@TOOL_ROOT@"/>
    <environment name="BINDIR" default="$QGRAF_BASE/bin"/>
  </client>
  <runtime name="PATH" default="$BINDIR" type="path"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post

