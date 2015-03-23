### RPM external cascade-toolfile 1.0
Requires: cascade
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/cascade.xml
<tool name="cascade" version="@TOOL_VERSION@">
  <architecture name="slc[^_]*_[^_]*_gcc4[0-3]">
    <lib name="cascade2"/>
    <lib name="bases"/>
    <lib name="mycern"/>
  </architecture>
  <architecture name="slc[^_]*_[^_]*_gcc4[4-9]">
    <lib name="cascade_merged"/>
  </architecture>
  <architecture name="^fc">
    <lib name="cascade_merged"/>
  </architecture>
  <architecture name="osx">
    <lib name="cascade_merged"/>
  </architecture>
  <client>
    <environment name="CASCADE_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$CASCADE_BASE/lib"/>
  </client>
  <runtime name="CASCADE_PDFPATH" value="$CASCADE_BASE/share"/>
  <use name="f77compiler"/>
  <use name="cascade_headers"/>
</tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%i/etc/scram.d/cascade_headers.xml
<tool name="cascade_headers" version="@TOOL_VERSION@">
  <client>
    <environment name="CASCADE_HEADERS_BASE" default="@TOOL_ROOT@"/>
    <environment name="INCLUDE" default="$CASCADE_HEADERS_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post

