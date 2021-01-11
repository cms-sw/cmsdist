### RPM external libpciaccess-toolfile 1.0
Requires: libpciaccess 

%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/libpciaccess.xml
<tool name="libpciaccess" version="@TOOL_VERSION@">
  <lib name="libpciaccess"/>
  <client>
    <environment name="LIBPCIACCESS_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR"            default="$LIBPCIACCESS_BASE/lib"/>
    <environment name="INCLUDE"           default="$LIBPCIACCESS_BASE/include"/>
  </client>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
