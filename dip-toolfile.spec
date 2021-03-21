### RPM external dip-toolfile 1.0
Requires: dip
%prep

%build

%install

mkdir -p %i/etc/scram.d

cat << \EOF_TOOLFILE >%i/etc/scram.d/dip_interface.xml
<tool name="dip_interface" version="@TOOL_VERSION@">
  <client>
    <environment name="DIP_INTERFACE_BASE" default="@TOOL_ROOT@"/>
    <environment name="INCLUDE"            default="$DIP_INTERFACE_BASE/include"/>
    <environment name="LIBDIR"             default="$DIP_INTERFACE_BASE/lib"/>
  </client>
</tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%i/etc/scram.d/dip.xml
<tool name="dip" version="@TOOL_VERSION@">
  <lib name="dip"/>
  <use name="dip_interface"/>
</tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%i/etc/scram.d/log4cplus.xml
<tool name="log4cplus" version="@TOOL_VERSION@">
  <lib name="log4cplus"/>
  <use name="dip_interface"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
