### RPM external meschach-toolfile 1.0
Requires: meschach
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/meschach.xml
<tool name="meschach" version="@TOOL_VERSION@">
  <info url="http://www.meschach.com"/>
  <lib name="meschach"/>
  <client>
    <environment name="MESCHACH_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$MESCHACH_BASE/lib"/>
    <environment name="INCLUDE" default="$MESCHACH_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
# bla bla
