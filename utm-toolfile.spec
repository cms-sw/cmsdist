### RPM external utm-toolfile 1.1
Requires: utm
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/utm.xml
<tool name="utm" version="@TOOL_VERSION@">
  <lib name="tmeventsetup"/>
  <lib name="tmtable"/>
  <lib name="tmxsd"/>
  <lib name="tmgrammar"/>
  <lib name="tmutil"/>
  <client>
    <environment name="UTM_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$UTM_BASE/lib"/>
    <environment name="INCLUDE" default="$UTM_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$INCLUDE" type="path"/>
  <runtime name="UTM_XSD_DIR" value="$UTM_BASE"/>
  <use name="root_cxxdefaults"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
# bla bla
