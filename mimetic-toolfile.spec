### RPM external mimetic-toolfile 1.0
Requires: mimetic
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/mimetic.xml
<tool name="mimetic" version="@TOOL_VERSION@">
  <lib name="mimetic"/>
  <client>
    <environment name="MIMETIC_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$MIMETIC_BASE/lib"/>
    <environment name="INCLUDE" default="$MIMETIC_BASE/include"/>
  </client>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
