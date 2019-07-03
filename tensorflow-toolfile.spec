### RPM external tensorflow-toolfile 2.0
Requires: tensorflow
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/tensorflow.xml
<tool name="tensorflow" version="@TOOL_VERSION@">
  <client>
    <environment name="TENSORFLOW_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$TENSORFLOW_BASE/lib"/>
    <environment name="INCLUDE" default="$TENSORFLOW_BASE/include"/>
    <environment name="INCLUDE" default="$TENSORFLOW_BASE/include/external/com_google_absl"/>
    <environment name="TFCOMPILE" default="$TENSORFLOW_BASE/bin/tfcompile"/>
  </client>
  <lib name="tensorflow_framework"/>
  <use name="eigen"/>
  <use name="protobuf"/>
  <runtime name="PATH" value="$TENSORFLOW_BASE/bin" type="path"/>
</tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%i/etc/scram.d/tensorflow-cc.xml
<tool name="tensorflow-cc" version="@TOOL_VERSION@">
  <lib name="tensorflow_cc"/>
  <use name="tensorflow"/>
</tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%i/etc/scram.d/tensorflow-c.xml
<tool name="tensorflow-c" version="@TOOL_VERSION@">
  <lib name="tensorflow"/>
  <use name="tensorflow"/>
</tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%i/etc/scram.d/tensorflow-runtime.xml
<tool name="tensorflow-runtime" version="@TOOL_VERSION@">
  <lib name="cpu_function_runtime"/>
  <use name="tensorflow"/>
</tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%i/etc/scram.d/tensorflow-xla_compiled_cpu_function.xml
<tool name="tensorflow-xla_compiled_cpu_function" version="@TOOL_VERSION@">
  <lib name="xla_compiled_cpu_function"/>
  <use name="tensorflow"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
