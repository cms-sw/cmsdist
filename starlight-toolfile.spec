### RPM external starlight-toolfile 1.0
Requires: starlight

%prep

%build

%install
mkdir -p %{i}/etc/scram.d
cat << \EOF_TOOLFILE >%{i}/etc/scram.d/starlight.xml
<tool name="starlight" version="@TOOL_VERSION@">
  <lib name="Starlib"/>
  <client>
    <environment name="STARLIGHT_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$STARLIGHT_BASE/lib"/>
    <environment name="INCLUDE" default="$STARLIGHT_BASE/include"/>
  </client>
  <runtime name="PATH" value="$STARLIGHT_BASE/bin" type="path"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
  <use name="clhep"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
# bla bla
