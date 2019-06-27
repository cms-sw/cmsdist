### RPM external dmtcp-toolfile 1.0
Requires: dmtcp
%prep

%build

%install

mkdir -p %{i}/etc/scram.d
cat << \EOF_TOOLFILE >%{i}/etc/scram.d/dmtcp.xml
<tool name="dmtcp" version="@TOOL_VERSION@">
  <info url="http://dmtcp.sourceforge.net/"/>
  <client>
    <environment name="DMTCP_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$DMTCP_BASE/lib"/>
    <environment name="LIBDIR" default="$DMTCP_BASE/lib/dmtcp"/>
  </client>
  <runtime name="PATH" value="$DMTCP_BASE/bin" type="path"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
# bla bla
