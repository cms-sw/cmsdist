### RPM external gccxml-toolfile 1.0
Requires: gccxml
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/gccxml.xml
<tool name="gccxml" version="@TOOL_VERSION@">
  <client>
    <environment name="GCCXML_BASE" default="@TOOL_ROOT@"/>
  </client>
  <runtime name="PATH" value="$GCCXML_BASE/bin" type="path"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
