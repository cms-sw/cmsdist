### RPM external tinyxml2-toolfile 1.0
Requires: tinyxml2

%prep
%build
%install
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/tinyxml2.xml
<tool name="tinyxml2" version="@TOOL_VERSION@">
  <info url="https://github.com/leethomason/tinyxml2"/>
  <lib name="tinyxml2"/>
  <client>
    <environment name="TINYXML2_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$TINYXML2_BASE/lib64"/>
    <environment name="INCLUDE" default="$TINYXML2_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$INCLUDE" type="path"/> 
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post

# bla bla
