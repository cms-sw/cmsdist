### RPM external alpgen-toolfile 1.0
Requires: alpgen
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/alpgen.xml
<tool name="alpgen" version="@TOOL_VERSION@">
  <client>
    <environment name="ALPGEN_BASE" default="@TOOL_ROOT@"/>
  </client>
  <runtime name="PATH" value="$ALPGEN_BASE/bin" type="path"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
# bla bla
