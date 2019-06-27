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
  </client>
  <use name="f77compiler"/>
  <use name="herwig"/>
  <use name="jimmy_headers"/>
</tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%i/etc/scram.d/jimmy_headers.xml
<tool name="jimmy_headers" version="@TOOL_VERSION@">
  <client>
    <environment name="JIMMY_HEADERS_BASE" default="@TOOL_ROOT@"/>
    <environment name="INCLUDE" default="$JIMMY_HEADERS_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post

# bla bla
