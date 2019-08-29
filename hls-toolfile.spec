### RPM external hls-toolfile 1.0
Requires: hls
%prep

%build

%install

mkdir -p %{i}/etc/scram.d
cat << \EOF_TOOLFILE >%{i}/etc/scram.d/hls.xml
<tool name="hls" version="@TOOL_VERSION@">
  <info url="https://github.com/Xilinx/HLS_arbitrary_Precision_Types"/>
  <client>
    <environment name="HLS_BASE" default="@TOOL_ROOT@"/>
    <environment name="INCLUDE" default="$HLS_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
