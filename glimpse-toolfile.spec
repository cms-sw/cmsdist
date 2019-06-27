### RPM external glimpse-toolfile 1.0
Requires: glimpse
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/glimpse.xml
<tool name="glimpse" version="@TOOL_VERSION@">
  <client>
    <environment name="GLIMPSE_BASE" default="@TOOL_ROOT@"/>
  </client>
  <runtime name="PATH" value="$GLIMPSE_BASE/bin" type="path"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
# bla bla
