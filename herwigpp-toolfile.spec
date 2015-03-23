### RPM external herwigpp-toolfile 1.0
Requires: herwigpp
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/herwigpp.xml
<tool name="herwigpp" version="@TOOL_VERSION@">
  <client>
    <environment name="HERWIGPP_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$HERWIGPP_BASE/lib"/>
    <environment name="INCLUDE" default="$HERWIGPP_BASE/include"/>
  </client>
  <runtime name="HERWIGPATH" value="$HERWIGPP_BASE/share/Herwig++"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post

