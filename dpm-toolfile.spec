### RPM external dpm-toolfile 1.0
Requires: dpm
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/dpm.xml
<tool name="dpm" version="@TOOL_VERSION@">
  <lib name="dpm"/>
  <client>
    <environment name="DPM_BASE" default="@TOOL_ROOT@"/>
    <environment name="INCLUDE" default="$DPM_BASE/include"/>
    <environment name="LIBDIR" default="$DPM_BASE/lib"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
# bla bla
