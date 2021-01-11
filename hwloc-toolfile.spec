### RPM external hwloc-toolfile 1.0
Requires: hwloc
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/hwloc.xml
<tool name="hwloc" version="@TOOL_VERSION@">
  <lib name="hwloc"/>
  <client>
    <environment name="HWLOC_BASE"  default="@TOOL_ROOT@"/>
    <environment name="INCLUDE"     default="$HWLOC_BASE/include/hwloc"/>
    <environment name="LIBDIR"      default="$HWLOC_BASE/lib"/>
  </client>
  <runtime name="PATH" value="$HWLOC_BASE/bin" type="path"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
