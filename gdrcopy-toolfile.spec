### RPM external gdrcopy-toolfile 1.0
Requires: gdrcopy
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/gdrcopy.xml
<tool name="gdrcopy" version="@TOOL_VERSION@">
  <lib name="gdrapi"/>
  <client>
    <environment name="GDRCOPY_BASE" default="@TOOL_ROOT@"/>
    <environment name="INCLUDE"      default="$GDRCOPY_BASE/include"/>
    <environment name="LIBDIR"       default="$GDRCOPY_BASE/lib64"/>
  </client>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
