### RPM external uuid-toolfile 1.0
Requires: uuid
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/uuid.xml
<tool name="uuid" version="@TOOL_VERSION@">
  <lib name="uuid"/>
  <client>
    <environment name="UUID_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$UUID_BASE/lib64"/>
    <environment name="INCLUDE" default="$UUID_BASE/include"/>
  </client>
  <use name="sockets"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
