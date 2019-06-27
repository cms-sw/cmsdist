### RPM external opencl-toolfile 1.0

Requires: opencl

%prep
# NOP

%build
# NOP

%install

mkdir -p %{i}/etc/scram.d
cat << \EOF_TOOLFILE >%{i}/etc/scram.d/opencl.xml
<tool name="opencl" version="@TOOL_VERSION@">
  <info url="https://www.khronos.org/opencl/"/>
  <lib name="OpenCL"/>
  <client>
    <environment name="OPENCL_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$OPENCL_BASE/lib64"/>
    <environment name="INCLUDE" default="$OPENCL_BASE/include"/>
  </client>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
# bla bla
