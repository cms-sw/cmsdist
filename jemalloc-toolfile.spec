### RPM external jemalloc-toolfile 1.0
Requires: jemalloc 
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/jemalloc.xml
<tool name="jemalloc" version="@TOOL_VERSION@">
  <architecture name="slc">
  <lib name="jemalloc"/>
  </architecture>
  <client>
    <environment name="JEMALLOC_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR"        default="$JEMALLOC_BASE/lib"/>
    <environment name="INCLUDE"        default="$JEMALLOC_BASE/include"/>
  </client>
  <runtime name="MALLOC_CONF" value="lg_chunk:18,lg_dirty_mult:4"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
