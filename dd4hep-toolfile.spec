### RPM external dd4hep-toolfile 1.0

Requires: dd4hep

%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/dd4hep.xml
<tool name="dd4hep" version="@TOOL_VERSION@">
  <info url="https://github.com/AIDASoft/DD4hep"/>
  <lib name="DDAlign" />
  <lib name="DDCore" />
  <lib name="DDCond" />
  <lib name="DDParsers" />
  <client>
    <environment name="DD4HEP_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$DD4HEP_BASE/lib"/>
    <environment name="INCLUDE" default="$DD4HEP_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$INCLUDE" type="path"/>
  <runtime name="PATH" value="$DD4HEP_BASE/bin" type="path"/>
  <use name="root_cxxdefaults"/>
  <use name="root"/>
  <use name="boost"/> 
  <use name="xerces-c"/>
  <use name="clhep"/>
</tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%i/etc/scram.d/dd4hep-cms.xml
<tool name="dd4hep-cms" version="@TOOL_VERSION@">
  <lib name="DDCMS" />
  <client>
    <environment name="DD4HEP_CMS_BASE" default="@TOOL_ROOT@"/>
  </client>
  <use name="dd4hep"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
