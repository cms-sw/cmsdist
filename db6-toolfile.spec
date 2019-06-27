### RPM external db6-toolfile 1.0
Requires: db6
%prep

%build

%install

mkdir -p %{i}/etc/scram.d
cat << \EOF_TOOLFILE >%{i}/etc/scram.d/db6.xml
<tool name="db6" version="@TOOL_VERSION@">
  <lib name="db"/>
  <client>
    <environment name="DB6_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$DB6_BASE/lib"/>
    <environment name="INCLUDE" default="$DB6_BASE/include"/>
    <environment name="BINDIR" default="$DB6_BASE/bin"/>
  </client>
  <runtime name="PATH" value="$BINDIR" type="path"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
# bla bla
