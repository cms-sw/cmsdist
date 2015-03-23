### RPM external tbb-toolfile 1.0
Requires: tbb 
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/tbb.xml
<tool name="tbb" version="@TOOL_VERSION@">
  <info url="http://threadingbuildingblocks.org"/>
  <lib name="tbb"/>
  <client>
    <environment name="TBB_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$TBB_BASE/lib"/>
    <environment name="INCLUDE" default="$TBB_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
