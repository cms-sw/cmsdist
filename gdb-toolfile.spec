### RPM external gdb-toolfile 1.0
Requires: gdb
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/gdb.xml
<tool name="gdb" version="@TOOL_VERSION@">
  <client>
    <environment name="GDB_BASE" default="@TOOL_ROOT@"/>
  </client>
  <runtime name="PATH" value="$GDB_BASE/bin" type="path"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
# bla bla
