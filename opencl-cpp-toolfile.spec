### RPM external opencl-cpp-toolfile 1.0

Requires: opencl-cpp

%prep
# NOP

%build
# NOP

%install

mkdir -p %{i}/etc/scram.d
cat << \EOF_TOOLFILE >%{i}/etc/scram.d/opencl-cpp.xml
<tool name="opencl-cpp" version="@TOOL_VERSION@">
  <info url="http://www.khronos.org/registry/cl/"/>
  <client>
    <environment name="OPENCL_CPP_BASE" default="@TOOL_ROOT@"/>
    <environment name="INCLUDE" default="$OPENCL_CPP_BASE/include"/>
  </client>
  <use name="opencl"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
# bla bla
