### RPM external json-toolfile 1.0
Requires: json

%prep

%build

%install
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE > %i/etc/scram.d/json.xml
<tool name="json" version="@TOOL_VERSION@">
  <client>
    <environment name="JSON_BASE" default="@TOOL_ROOT@"/>
    <environment name="INCLUDE"   default="$JSON_BASE/include"/>
  </client>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
