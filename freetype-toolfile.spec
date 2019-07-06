### RPM external freetype-toolfile 1.0
Requires: freetype
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/freetype.xml
<tool name="freetype" version="@TOOL_VERSION@">
  <lib name="freetype-cms"/>
  <client>
    <environment name="FREETYPE_BASE" default="@TOOL_ROOT@"/>
    <environment name="INCLUDE"      default="$FREETYPE_BASE/include"/>
    <environment name="LIBDIR"       default="$FREETYPE_BASE/lib"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
