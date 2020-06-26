### RPM external highfive-toolfile 1.0
Requires: highfive
%prep

%build

%install

mkdir -p %{i}/etc/scram.d
cat << \EOF_TOOLFILE >%{i}/etc/scram.d/highfive.xml
<tool name="highfive" version="@TOOL_VERSION@">
  <info url="https://github.com/BlueBrain/HighFive"/>
  <client>
    <environment name="HIGHFIVE_BASE" default="@TOOL_ROOT@"/>
    <environment name="INCLUDE" default="$HIGHFIVE_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$INCLUDE" type="path"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
