### RPM external tensorflow-cc-toolfile 1.0
Requires: tensorflow-cc
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/tensorflow-cc.xml
<tool name="tensorflow-cc" version="@TOOL_VERSION@">
  <lib name="tensorflow_cc"/>
  <lib name="tensorflow_framework"/>
  <client>
    <use name="tensorflow-c"/>
    <use name="eigen"/>
    <use name="protobuf"/>
    <environment name="TENSORFLOW_CC_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$TENSORFLOW_CC_BASE/tensorflow_cc/lib"/>
    <environment name="INCLUDE" default="$TENSORFLOW_CC_BASE/tensorflow_cc/include"/>
  </client>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
