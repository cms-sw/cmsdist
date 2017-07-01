### RPM external tensorflow-c-toolfile 1.0
Requires: tensorflow-c
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/tensorflow-c.xml
<tool name="tensorflow-c" version="@TOOL_VERSION@">
  <lib name="tensorflow"/>
  <client>
    <environment name="TENSORFLOW_C_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$TENSORFLOW_C_BASE/lib"/>
    <environment name="INCLUDE" default="$TENSORFLOW_C_BASE/include"/>
  </client>
</tool>
EOF_TOOLFILE


## IMPORT scram-tools-post
