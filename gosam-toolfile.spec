### RPM external gosam-toolfile 2.0
Requires: gosam
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/gosam.xml
<tool name="gosam" version="@TOOL_VERSION@">
  <client>
    <environment name="GOSAM_BASE" default="@TOOL_ROOT@"/>
    <environment name="BINDIR" default="$GOSAM_BASE/bin"/>
  </client>
  <runtime name="PATH" default="$BINDIR" type="path"/>
</tool>
EOF_TOOLFILE

export PYTHONV=$(echo $PYTHON_VERSION | cut -f1,2 -d.)

## IMPORT scram-tools-post
