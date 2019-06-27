### RPM external py2-dablooms-toolfile 1.0
Requires: py2-dablooms

%prep

%build

%install

mkdir -p %{i}/etc/scram.d
cat << \EOF_TOOLFILE >%{i}/etc/scram.d/dablooms.xml
<tool name="dablooms" version="@TOOL_VERSION@">
  <lib name="dablooms"/>
  <client>
    <environment name="PY2_DABLOOMS_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$PY2_DABLOOMS_BASE/lib"/>
    <environment name="INCLUDE" default="$PY2_DABLOOMS_BASE/include"/>
  </client>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
# bla bla
