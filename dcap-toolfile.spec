### RPM external dcap-toolfile 1.0
Requires: dcap
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/dcap.xml
<tool name="dcap" version="@TOOL_VERSION@">
  <lib name="dcap"/>
  <client>
    <environment name="DCAP_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$DCAP_BASE/lib"/>
    <environment name="INCLUDE" default="$DCAP_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
# bla bla
