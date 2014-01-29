### RPM external soqt-toolfile 1.0
Requires: soqt
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/soqt.xml
<tool name="soqt" version="@TOOL_VERSION@">
  <info url="http://www.coin3d.org"/>
  <lib name="SoQt"/>
  <client>
    <environment name="SOQT_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$SOQT_BASE/lib"/>
    <environment name="INCLUDE" default="$SOQT_BASE/include"/>
  </client>
  <use name="OpenInventor"/>
  <use name="Qt"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
