### RPM external tinyxml-toolfile 1.0
Requires: tinyxml

%prep
%build
%install
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/tinyxml.xml
<tool name="tinyxml" version="@TOOL_VERSION@">
  <info url="https://sourceforge.net/projects/tinyxml/"/>
   <lib name="tinyxml"/>
  <client>
    <environment name="TINYXML_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$TINYXML_BASE/lib"/>
    <environment name="INCLUDE" default="$TINYXML_BASE/include"/>
  </client>  
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post

