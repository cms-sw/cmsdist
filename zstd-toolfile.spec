### RPM external zstd-toolfile 1.0
Requires: zstd
%prep

%build

%install

mkdir -p %{i}/etc/scram.d
cat << \EOF_TOOLFILE >%{i}/etc/scram.d/zstd.xml
<tool name="zstd" version="@TOOL_VERSION@">
  <info url="http://https://facebook.github.io/zstd"/>
  <lib name="zstd"/>
  <client>
    <environment name="ZSTD_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$ZSTD_BASE/lib"/>
    <environment name="INCLUDE" default="$ZSTD_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$INCLUDE" type="path"/>
  <runtime name="PATH" value="$ZSTD_BASE/bin" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
