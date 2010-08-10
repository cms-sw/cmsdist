### RPM external jimmy-toolfile 1.0
Requires: jimmy
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/jimmy.xml
<tool name="jimmy" version="@TOOL_VERSION@">
  <lib name="jimmy"/>
  <client>
    <environment name="JIMMY_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$JIMMY_BASE/lib"/>
    <environment name="INCLUDE" default="$JIMMY_BASE/include"/>
  </client>
  <use name="f77compiler"/>
  <use name="herwig"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
