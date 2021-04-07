### RPM external tbb-toolfile 2.0
Requires: tbb 
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/tbb.xml
<tool name="tbb" version="@TOOL_VERSION@">
  <info url="http://threadingbuildingblocks.org"/>
  <lib name="tbb"/>
  <client>
    <environment name="TBB_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR"   default="$TBB_BASE/lib"/>
    <environment name="INCLUDE"  default="$TBB_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
  <flags CPPDEFINES="TBB_USE_GLIBCXX_VERSION=@GCC_GLIBCXX_VERSION@"/>
  <flags CPPDEFINES="TBB_SUPPRESS_DEPRECATED_MESSAGES"/>
  <flags CPPDEFINES="TBB_PREVIEW_RESUMABLE_TASKS=1"/>
  <flags SYSTEM_INCLUDE="1"/>
</tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%i/etc/scram.d/tbbbind.xml
<tool name="tbbbind" version="@TOOL_VERSION@">
  <info url="http://threadingbuildingblocks.org"/>
  <use name="tbb"/>
  <lib name="tbbbind_2_0"/>
  <client>
    <environment name="TBBBIND_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR"       default="$TBBBIND_BASE/lib"/>
    <environment name="INCLUDE"      default="$TBBBIND_BASE/include"/>
  </client>
  <flags SYSTEM_INCLUDE="1"/>
</tool>
EOF_TOOLFILE

export GCC_GLIBCXX_VERSION=$(gcc -dumpversion | tr '.' '0')

## IMPORT scram-tools-post
