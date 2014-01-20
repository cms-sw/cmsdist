### RPM external yamlcpp-toolfile 1.0
Requires: yamlcpp
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/yamlcpp.xml
<tool name="yamlcpp" version="@TOOL_VERSION@">
  <lib name="yaml-cpp"/>
  <client>
    <environment name="YAMLCPP_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$YAMLCPP_BASE/lib"/>
    <environment name="INCLUDE" default="$YAMLCPP_BASE/include"/>
  </client>
  <use name="cxxcompiler"/>
  <use name="boost"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
