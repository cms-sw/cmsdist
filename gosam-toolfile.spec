### RPM external gosam-toolfile 2.0
Requires: gosam
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/gosam.xml
<tool name="gosam" version="@TOOL_VERSION@">
  <client>
    <environment name="GOSAM_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$GOSAM_BASE/lib"/>
    <environment name="INCLUDE" default="$GOSAM_BASE/include"/>
    <environment name="BINDIR" default="$GOSAM_BASE/bin"/>
  </client>
<runtime name="PATH" default="$BINDIR" type="path"/>
<use name="python"/>
<use name="cython"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post


