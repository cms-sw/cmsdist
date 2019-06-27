### RPM external xerces-c-toolfile 1.0
Requires: xerces-c
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/xerces-c.xml
<tool name="xerces-c" version="@TOOL_VERSION@">
  <info url="http://xml.apache.org/xerces-c/"/>
  <lib name="xerces-c"/>
  <client>
    <environment name="XERCES_C_BASE" default="@TOOL_ROOT@"/>
    <environment name="INCLUDE" default="$XERCES_C_BASE/include"/>
    <environment name="LIBDIR" default="$XERCES_C_BASE/lib"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
# bla bla
