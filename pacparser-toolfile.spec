### RPM external pacparser-toolfile 1.0
Requires: pacparser
%prep

%build

%install

mkdir -p %{i}/etc/scram.d
cat << \EOF_TOOLFILE >%{i}/etc/scram.d/pacparser.xml
<tool name="pacparser" version="@TOOL_VERSION@">
  <info url="http://code.google.com/p/pacparser/"/>
  <lib name="pacparser"/>
  <client>
    <environment name="PACPARSER_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$PACPARSER_BASE/lib"/>
    <environment name="INCLUDE" default="$PACPARSER_BASE/include"/>
  </client>
  <runtime name="PATH" value="$PACPARSER_BASE/bin" type="path"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
# bla bla
