### RPM external codecompass-toolfile 1.0

Requires: codecompass boost-toolfile thrift-toolfile odb-toolfile python-toolfile sqlite-toolfile graphviz-toolfile libgit2-toolfile

%prep

%build

%install

mkdir -p %{i}/etc/scram.d
cat << \EOF_TOOLFILE >%{i}/etc/scram.d/codecompass.xml
  <tool name="codecompass" version="@TOOL_VERSION@">
    <client>
      <environment name="CODECOMPASS_BASE" default="@TOOL_ROOT@"/>
    </client>
    <runtime name="CODECOMPASS_BASE" default="@TOOL_ROOT@"/>
  </tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
