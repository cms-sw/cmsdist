### RPM external ucx-toolfile 1.0
Requires: ucx
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/ucx.xml
<tool name="ucx" version="@TOOL_VERSION@">
  <lib name="ucp"/>
  <lib name="uct"/>
  <lib name="ucs"/>
  <lib name="ucm"/>
  <client>
    <environment name="UCX_BASE" default="@TOOL_ROOT@"/>
    <environment name="INCLUDE"  default="$UCX_BASE/include"/>
    <environment name="LIBDIR"   default="$UCX_BASE/lib"/>
  </client>
  <runtime name="PATH" value="$UCX_BASE/bin" type="path"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
