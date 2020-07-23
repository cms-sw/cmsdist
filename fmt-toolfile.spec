### RPM external fmt-toolfile 1.0
Requires: fmt
%prep

%build

%install

mkdir -p %{i}/etc/scram.d
cat << \EOF_TOOLFILE >%{i}/etc/scram.d/fmt.xml
<tool name="fmt" version="@TOOL_VERSION@">
  <info url="https://github.com/fmtlib/fmt"/>
  <lib name="fmt"/>
  <client>
    <environment name="FMT_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$FMT_BASE/lib"/>
    <environment name="INCLUDE" default="$FMT_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$INCLUDE" type="path"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
