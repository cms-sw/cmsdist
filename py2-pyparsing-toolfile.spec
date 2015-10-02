### RPM external py2-pyparsing-toolfile 1.0
Requires: py2-pyparsing
%prep

%build

%install

mkdir -p %{i}/etc/scram.d
cat << \EOF_TOOLFILE >%{i}/etc/scram.d/py2-pyparsing.xml
<tool name="py2-pyparsing" version="@TOOL_VERSION@">
  <info url="https://pyparsing.wikispaces.com/"/>
  <client>
    <environment name="PY2_PYPARSING" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$PY2_PYPARSING/lib"/>
    <runtime name="PYTHONPATH" value="$PY2_PYPARSING/lib/python@PYTHONV@/site-packages" type="path"/>
  </client>
</tool>
EOF_TOOLFILE

export PYTHONV=$(echo $PYTHON_VERSION | cut -f1,2 -d.)

## IMPORT scram-tools-post
