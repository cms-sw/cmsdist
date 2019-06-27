### RPM cms das_client-toolfile 1.0
Requires: das_client
%prep
%build
%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/das_client.xml
<tool name="das_client" version="@TOOL_VERSION@">
  <client>
    <environment name="DAS_CLIENT_BASE" default="@TOOL_ROOT@"/>
  </client>
  <runtime name="PATH"       value="$DAS_CLIENT_BASE/bin" type="path"/>
  <use name="python"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
# bla bla
