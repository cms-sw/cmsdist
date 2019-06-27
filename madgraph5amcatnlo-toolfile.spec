### RPM external madgraph5amcatnlo-toolfile 1.0
Requires: madgraph5amcatnlo
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/madgraph5amcatnlo.xml
<tool name="madgraph5amcatnlo" version="@TOOL_VERSION@">
  <client>
    <environment name="MADGRAPH5AMCATNLO_BASE" default="@TOOL_ROOT@"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$MADGRAPH5AMCATNLO_BASE" type="path"/>
  <runtime name="ROOT_PATH" value="$MADGRAPH5AMCATNLO_BASE" type="path"/>
  <use name="root_cxxdefaults"/>
  <use name="gosamcontrib"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
# bla bla
