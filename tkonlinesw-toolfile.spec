### RPM external tkonlinesw-toolfile 1.0
Requires: tkonlinesw
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/tkonlinesw.xml
<tool name="TkOnlineSw" version="@TOOL_VERSION@">
  <info url="http://www.cern.ch/"/>
  <lib name="ICUtils"/>
  <lib name="Fed9UUtils"/>
  <client>
    <environment name="TKONLINESW_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" value="$TKONLINESW_BASE/lib"/>
    <environment name="INCLUDE" value="$TKONLINESW_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$INCLUDE" type="path"/>
  <flags CXXFLAGS="-DCMS_TK_64BITS"/>
  <use name="root_cxxdefaults"/>
  <use name="xerces-c"/>
</tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%i/etc/scram.d/tkonlineswdb.xml
<tool name="TkOnlineSwDB" version="@TOOL_VERSION@">
  <info url="http://www.cern.ch/"/>
  <lib name="DeviceDescriptions"/>
  <lib name="Fed9UDeviceFactory"/>
  <use name="tkonlinesw"/>
  <use name="oracle"/>
  <use name="oracleocci"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
# bla bla
