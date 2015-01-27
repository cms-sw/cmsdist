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
  <runtime name="LHAPATH" value="$LHAPDF_BASE/share/lhapdf/PDFsets"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
  <use name="f77compiler"/>
</tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%i/etc/scram.d/lhapdfwrap.xml
<tool name="lhapdfwrap" version="@TOOL_VERSION@">
  <lib name="LHAPDFWrap"/>
  <use name="lhapdf"/>
</tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%i/etc/scram.d/lhapdffull.xml
<tool name="lhapdffull" version="@TOOL_VERSION@">
  <lib name="LHAPDF"/>
  <client>
    <environment name="LHAPDFFULL_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$LHAPDFFULL_BASE/full/lib"/>
    <environment name="INCLUDE" default="$LHAPDFFULL_BASE/include"/>
  </client>
  <runtime name="LHAPATH" value="$LHAPDFFULL_BASE/share/lhapdf/PDFsets"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
  <use name="f77compiler"/>
</tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%i/etc/scram.d/lhapdfwrapfull.xml
<tool name="lhapdfwrapfull" version="@TOOL_VERSION@">
  <lib name="LHAPDFWrap"/>
  <use name="lhapdffull"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
