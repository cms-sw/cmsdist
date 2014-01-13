### RPM cms vdt-toolfile 1.0
Requires: vdt
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/vdt.xml
<tool name="vdt" version="@TOOL_VERSION@">
  <lib name="vdt"/>
  <client>
    <environment name="VDT_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$VDT_BASE/lib"/>
    <environment name="INCLUDE" default="$VDT_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post

