### RPM external das-client-toolfile 1.0
Requires: das-client
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/das-client.xml
<tool name="das-client" version="@TOOL_VERSION@">
  <client>
    <environment name="DAS_CLIENT_BASE" default="@TOOL_ROOT@"/>
  </client>
  <runtime name="PATH" value="$DAS_CLIENT_BASE/bin" type="path"/>
  <runtime name="PYTHONPATH" value="$DAS_CLIENT_BASE/bin" type="path"/>
  <use name="python"/>
</tool>
EOF_TOOLFILE

export PYTHONV=$(echo $PYTHON_VERSION | cut -f1,2 -d.)


## IMPORT scram-tools-post
