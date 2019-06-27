### RPM external mcdb-toolfile 1.0
Requires: mcdb
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/mcdb.xml
<tool name="mcdb" version="@TOOL_VERSION@">
  <lib name="mcdb"/>
  <client>
    <environment name="MCDB_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$MCDB_BASE/lib"/>
    <environment name="INCLUDE" default="$MCDB_BASE/interface"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
  <use name="xerces-c"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
# bla bla
