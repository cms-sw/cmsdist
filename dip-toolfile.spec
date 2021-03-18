### RPM external dip-toolfile 1.0
Requires: dip
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/dip.xml
<tool name="dip" version="@TOOL_VERSION@">
  <lib name="dip"/>
  <client>
    <environment name="DIP_BASE" default="@TOOL_ROOT@"/>
    <environment name="INCLUDE"      default="$DIP_BASE/include"/>
    <environment name="LIBDIR"       default="$DIP_BASE/lib"/>
  </client>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
