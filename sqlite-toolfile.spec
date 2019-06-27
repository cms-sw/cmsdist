### RPM external sqlite-toolfile 1.0
Requires: sqlite
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/sqlite.xml
<tool name="sqlite" version="@TOOL_VERSION@">
  <lib name="sqlite3"/>
  <client>
    <environment name="SQLITE_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$SQLITE_BASE/lib"/>
    <environment name="BINDIR" default="$SQLITE_BASE/bin"/>
    <environment name="INCLUDE" default="$SQLITE_BASE/include"/>
  </client>
  <runtime name="PATH" value="$BINDIR" type="path"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
# bla bla
