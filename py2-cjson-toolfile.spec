### RPM external py2-cjson-toolfile 1.0
Requires: py2-cjson
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/py2-cjson.xml
<tool name="py2-cjson" version="@TOOL_VERSION@">
  <client>
    <environment name="PY2_CJSON_BASE" default="@TOOL_ROOT@"/>
  </client>
  <runtime name="PYTHONPATH" value="$PY2_CJSON_BASE/lib/python@PYTHONV@/site-packages" type="path"/>
  <use name="python"/>
</tool>
EOF_TOOLFILE

export PYTHONV=$(echo $PYTHON_VERSION | cut -f1,2 -d.)

## IMPORT scram-tools-post

