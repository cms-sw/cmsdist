### RPM external lhapdf6-toolfile 1.0
Requires: lhapdf6
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/lhapdf6.xml
<tool name="lhapdf6" version="@TOOL_VERSION@">
  <lib name="LHAPDF"/>
  <client>
    <environment name="LHAPDF6_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$LHAPDF6_BASE/lib"/>
    <environment name="INCLUDE" default="$LHAPDF6_BASE/include"/>
  </client>
  <runtime name="LHAPDF_DATA_PATH" value="$LHAPDF6_BASE/share/LHAPDF"/>
  <use name="yaml-cpp"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
