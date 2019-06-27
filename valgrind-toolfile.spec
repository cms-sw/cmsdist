### RPM external valgrind-toolfile 1.0
Requires: valgrind
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/valgrind.xml
<tool name="valgrind" version="@TOOL_VERSION@">
  <client>
    <environment name="VALGRIND_BASE" default="@TOOL_ROOT@"/>
    <environment name="INCLUDE" default="$VALGRIND_BASE/include"/>
  </client>
  <runtime name="PATH" value="$VALGRIND_BASE/bin" type="path"/>
  <runtime name="VALGRIND_LIB" value="$VALGRIND_BASE/lib/valgrind"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
# bla bla
