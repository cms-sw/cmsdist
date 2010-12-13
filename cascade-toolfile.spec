### RPM external cascade-toolfile 1.0
Requires: cascade
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/cascade.xml
<tool name="cascade" version="@TOOL_VERSION@">
  <lib name="cascade2"/>
  <lib name="bases"/>
  <lib name="mycern"/>
  <client>
    <environment name="CASCADE_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$CASCADE_BASE/lib"/>
    <environment name="INCLUDE" default="$CASCADE_BASE/include"/>
    <environment name="PDFPATH" default="$CASCADE_BASE/share"/>
  </client>
  <use name="f77compiler"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
