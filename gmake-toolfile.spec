### RPM external gmake-toolfile 1.0
Requires: gmake
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/gmake.xml
<tool name="gmake" version="@TOOL_VERSION@">
  <client>
    <environment name="MAKE_BASE" default="@TOOL_ROOT@"/>
  </client>
  <runtime name="PATH" value="$MAKE_BASE/bin" type="path"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
# bla bla
