### RPM external py2-cx-oracle-toolfile 1.0
Requires: py2-cx-oracle
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/py2-cx-oracle.xml
<tool name="py2-cx-oracle" version="@TOOL_VERSION@">
  <client>
    <environment name="PY2_CX_ORACLE_BASE" default="@TOOL_ROOT@"/>
  </client>
  <use name="python"/>
  <use name="oracle"/>
</tool>
EOF_TOOLFILE

export PYTHONV=$(echo $PYTHON_VERSION | cut -f1,2 -d.)

## IMPORT scram-tools-post

