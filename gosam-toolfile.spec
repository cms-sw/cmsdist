### RPM external gosam-toolfile 2.0
Requires: gosam
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/gosam.xml
<tool name="gosam" version="@TOOL_VERSION@">
  <lib name="GoSam"/>
  <client>
    <environment name="GOSAM_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$GOSAM_BASE/lib"/>
    <environment name="INCLUDE" default="$GOSAM_BASE/include"/>
  </client>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post

