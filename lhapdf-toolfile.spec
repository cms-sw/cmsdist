### RPM external lhapdf-toolfile 1.0
Requires: lhapdf
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/lhapdf.xml
<tool name="lhapdf" version="@TOOL_VERSION@">
  <lib name="LHAPDF"/>
  <client>
    <environment name="LHAPDF_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$LHAPDF_BASE/lib"/>
    <environment name="INCLUDE" default="$LHAPDF_BASE/include"/>
  </client>
  <runtime name="LHAPDF_DATA_PATH" value="$LHAPDF_BASE/share/LHAPDF"/>
  <use name="yaml-cpp"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
