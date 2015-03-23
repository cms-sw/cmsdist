### RPM external db4-toolfile 1.0
Requires: db4
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/db4.xml
<tool name="db4" version="@TOOL_VERSION@">
  <lib name="db"/>
  <client>
    <environment name="DB4_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$DB4_BASE/lib"/>
    <environment name="INCLUDE" default="$DB4_BASE/include"/>
    <environment name="BINDIR" default="$DB4_BASE/bin"/>
  </client>
  <runtime name="PATH" value="$BINDIR" type="path"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
