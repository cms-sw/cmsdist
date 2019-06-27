### RPM cms vdt-toolfile 1.0
Requires: vdt
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/vdt_headers.xml
<tool name="vdt_headers" version="@TOOL_VERSION@">
  <client>
    <environment name="VDT_HEADERS_BASE" default="@TOOL_ROOT@"/>
    <environment name="INCLUDE" default="$VDT_HEADERS_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%i/etc/scram.d/vdt.xml
<tool name="vdt" version="@TOOL_VERSION@">
  <lib name="vdt"/>
  <use name="vdt_headers"/>
  <client>
    <environment name="VDT_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$VDT_BASE/lib"/>
  </client>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
# bla bla
