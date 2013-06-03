### RPM cms rulechecker-toolfile 1.0
Requires: rulechecker
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/rulechecker.xml
<tool name="rulechecker" version="@TOOL_VERSION@">
  <client>
    <environment name="RULECHECKER_BASE" default="@TOOL_ROOT@"/>
  </client>
  <runtime name="CLASSPATH" value="$RULECHECKER_BASE" type="path"/>
  <runtime name="RULECHECKER_PREPROCESS_EXT" value="i"/>
  <runtime name="RULECHECKER_VIOLATION_EXT" value="viol"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
