### RPM external libuuid-toolfile 1.0
Requires: libuuid
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/libuuid.xml
<tool name="libuuid" version="@TOOL_VERSION@">
  <lib name="uuid"/>
  <client>
    <environment name="LIBUUID_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$LIBUUID_BASE/lib64"/>
    <environment name="INCLUDE" default="$LIBUUID_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
  <use name="sockets"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
# bla bla
