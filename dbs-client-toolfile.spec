### RPM cms dbs-client-toolfile 1.0
Requires: dbs-client
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/dbs-client.xml
<tool name="dbs-client" version="@TOOL_VERSION@">
  <client>
    <environment name="DBS_CLIENT_BASE" default="@TOOL_ROOT@"/>
  </client>
  <runtime name="PATH" value="$DBS_CLIENT_BASE/bin" type="path"/>
  <runtime name="PYTHONPATH" value="$DBS_CLIENT_BASE/lib" type="path"/>
  <runtime name="PYTHONPATH" value="$DBS_CLIENT_BASE/lib/DBSAPI" type="path"/>
  <runtime name="DBS_CLIENT_CONFIG" value="$DBS_CLIENT_BASE/lib/DBSAPI/dbs.config"/>
  <runtime name="DBSCMD_HOME" value="$DBS_CLIENT_BASE/lib/DBSAPI"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
