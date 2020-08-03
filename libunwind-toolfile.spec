### RPM external libunwind-toolfile 1.0
Requires: libunwind
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/libunwind.xml
<tool name="libunwind" version="@TOOL_VERSION@">
  <lib name="unwind"/>
  <client>
    <environment name="LIBUNWIND_BASE" default="@TOOL_ROOT@"/>
    <environment name="INCLUDE"      default="$LIBUNWIND_BASE/include"/>
    <environment name="LIBDIR"       default="$LIBUNWIND_BASE/lib"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
