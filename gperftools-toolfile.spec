### RPM external gperftools-toolfile 2.0

Requires: gperftools

%prep

%build

%install

mkdir -p %{i}/etc/scram.d
cat << \EOF_TOOLFILE >%{i}/etc/scram.d/tcmalloc_minimal.xml
<tool name="tcmalloc_minimal" version="@TOOL_VERSION@">
  <lib name="tcmalloc_minimal"/>
  <client>
    <environment name="TCMALLOC_MINIMAL_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR"                default="$TCMALLOC_MINIMAL_BASE/lib"/>
  </client>
</tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%{i}/etc/scram.d/tcmalloc.xml
<tool name="tcmalloc" version="@TOOL_VERSION@">
  <lib name="tcmalloc"/>
  <client>
    <environment name="TCMALLOC_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR"        default="$TCMALLOC_BASE/lib"/>
  </client>
</tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%{i}/etc/scram.d/gperf.xml
<tool name="gperf" version="@TOOL_VERSION@">
  <lib name="profiler"/>
  <client>
    <environment name="GPERF_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR"        default="$GPERF_BASE/lib"/>
  </client>
  <runtime name="PATH" value="$GPERF_BASE/bin" type="path"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
