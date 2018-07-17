### RPM external odb-toolfile 1.0
Requires: odb
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/odb.xml
<tool name="odb" version="@TOOL_VERSION@">
  <info url="http://www.research.att.com/sw/tools/odb/"/>
  <lib name="cutl"/>
  <lib name="odb"/>
  <lib name="odb-sqlite"/>
  <client>
    <environment name="ODB_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$ODB_BASE/lib"/>
    <environment name="INCLUDE" default="$ODB_BASE/include"/>
  </client>
  <runtime name="PATH" value="$ODB_BASE/bin" type="path"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
