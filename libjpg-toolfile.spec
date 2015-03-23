### RPM external libjpg-toolfile 1.0
Requires: libjpg
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/libjpg.xml
<tool name="libjpg" version="@TOOL_VERSION@">
  <info url="http://www.ijg.org/"/>
  <lib name="jpeg"/>
  <client>
    <environment name="LIBJPEG_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$LIBJPEG_BASE/lib"/>
    <environment name="INCLUDE" default="$LIBJPEG_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
