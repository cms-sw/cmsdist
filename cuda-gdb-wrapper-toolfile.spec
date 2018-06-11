### RPM external cuda-gdb-wrapper-toolfile 1.0
Requires: cuda-gdb-wrapper

%prep

%build

%install
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/cuda-gdb-wrapper.xml
<tool name="cuda-gdb-wrapper" version="@TOOL_VERSION@">
  <client>
    <environment name="CUDA_GDB_WRAPPER_BASE" default="@TOOL_ROOT@"/>
  </client>
  <runtime name="PATH" value="$CUDA_GDB_WRAPPER_BASE/bin" type="path"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
