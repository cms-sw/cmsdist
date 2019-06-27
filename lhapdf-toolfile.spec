### RPM external lhapdf-toolfile 1.0
Requires: lhapdf
%prep

%build

%install
export PYTHON_LIB_SITE_PACKAGES
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/lhapdf.xml
<tool name="lhapdf" version="@TOOL_VERSION@">
  <lib name="LHAPDF"/>
  <client>
    <environment name="LHAPDF_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$LHAPDF_BASE/lib"/>
    <environment name="INCLUDE" default="$LHAPDF_BASE/include"/>
  </client>
  <use name="yaml-cpp"/>
  <runtime name="LHAPDF_DATA_PATH" value="$LHAPDF_BASE/share/LHAPDF"/>
  <runtime name="PATH" value="$LHAPDF_BASE/bin" type="path"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
# bla bla
