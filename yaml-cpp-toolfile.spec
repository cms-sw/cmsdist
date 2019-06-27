### RPM external yaml-cpp-toolfile 1.0
Requires: yaml-cpp
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/yaml-cpp.xml
<tool name="yaml-cpp" version="@TOOL_VERSION@">
  <info url="http://code.google.com/p/yaml-cpp/"/>
  <lib name="yaml-cpp"/>
  <client>
    <environment name="YAML_CPP_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$YAML_CPP_BASE/lib"/>
    <environment name="INCLUDE" default="$YAML_CPP_BASE/include"/>
  </client>
  <use name="boost"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
# bla bla
