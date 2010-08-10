### RPM external toprex-toolfile 1.0
Requires: toprex
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/toprex.xml
<tool name="toprex" version="@TOOL_VERSION@">
  <lib name="toprex"/>
  <client>
    <environment name="TOPREX_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$TOPREX_BASE/lib"/>
    <environment name="INCLUDE" default="$TOPREX_BASE/include"/>
  </client>
  <use name="f77compiler"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
