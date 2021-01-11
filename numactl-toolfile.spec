### RPM external numactl-toolfile 1.0
Requires: numactl
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/numactl.xml
<tool name="numactl" version="@TOOL_VERSION@">
  <lib name="numa"/>
  <client>
    <environment name="NUMACTL_BASE" default="@TOOL_ROOT@"/>
    <environment name="INCLUDE"      default="$NUMACTL_BASE/include"/>
    <environment name="LIBDIR"       default="$NUMACTL_BASE/lib"/>
  </client>
  <runtime name="PATH" value="$NUMACTL_BASE/bin" type="path"/>
  <runtime name="MANPATH" value="$NUMACTL_BASE/share/man" type="path"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
