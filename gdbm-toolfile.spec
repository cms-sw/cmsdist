### RPM external gdbm-toolfile 1.0
Requires: gdbm
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/gdbm.xml
<tool name="gdbm" version="@TOOL_VERSION@">
  <lib name="gdbm"/>
  <client>
    <environment name="GDBM_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$GDBM_BASE/lib"/>
    <environment name="INCLUDE" default="$GDBM_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
# bla bla
