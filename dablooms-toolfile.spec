### RPM external dablooms-toolfile 1.0
Requires: dablooms

%prep

%build

%install

mkdir -p %{i}/etc/scram.d
cat << \EOF_TOOLFILE >%{i}/etc/scram.d/dablooms.xml
<tool name="dablooms" version="@TOOL_VERSION@">
  <lib name="dablooms"/>
  <client>
    <environment name="DABLOOMS_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$DABLOOMS_BASE/lib"/>
    <environment name="INCLUDE" default="$DABLOOMS_BASE/include"/>
  </client>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
