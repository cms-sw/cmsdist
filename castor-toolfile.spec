### RPM external castor-toolfile 2.0
Requires: castor
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/castor_header.xml
<tool name="castor_header" version="@TOOL_VERSION@">
  <client>
    <environment name="CASTOR_HEADER_BASE" default="@TOOL_ROOT@"/>
    <environment name="INCLUDE" default="$CASTOR_HEADER_BASE/include"/>
    <environment name="INCLUDE" default="$CASTOR_HEADER_BASE/include/shift"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$CASTOR_HEADER_BASE/include" type="path"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$CASTOR_HEADER_BASE/include/shift" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>
EOF_TOOLFILE
cat << \EOF_TOOLFILE >%i/etc/scram.d/castor.xml
<tool name="castor" version="@TOOL_VERSION@">
  <lib name="shift"/>
  <lib name="castorrfio"/>
  <lib name="castorclient"/>
  <lib name="castorcommon"/>
  <client>
    <environment name="CASTOR_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$CASTOR_BASE/lib"/>
  </client>
  <runtime name="PATH" value="$CASTOR_BASE/bin" type="path"/>
  <use name="castor_header"/>
  <use name="libuuid"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
# bla bla
