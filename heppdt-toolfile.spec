### RPM external heppdt-toolfile 1.0
Requires: heppdt
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/heppdt.xml
<tool name="heppdt" version="@TOOL_VERSION@">
  <lib name="HepPDT"/>
  <lib name="HepPID"/>
  <client>
    <environment name="HEPPDT_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$HEPPDT_BASE/lib"/>
    <environment name="INCLUDE" default="$HEPPDT_BASE/include"/>
  </client>
  <runtime name="HEPPDT_PARAM_PATH" value="$HEPPDT_BASE"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
# bla bla
