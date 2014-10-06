### RPM external py2-ordereddict-toolfile 1.0
Requires: py2-ordereddict
%prep

%build

%install

mkdir -p %{i}/etc/scram.d
cat << \EOF_TOOLFILE >%{i}/etc/scram.d/py2-ordereddict.xml
<tool name="py2-ordereddict" version="@TOOL_VERSION@">
  <info url="https://pypi.python.org/pypi/MarkupSafe"/>
  <client>
    <environment name="PY2_ORDEREDDICT_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$PY2_ORDEREDDICT_BASE/lib"/>
    <runtime name="PYTHONPATH" value="$PY2_ORDEREDDICT_BASE/lib/python@PYTHONV@/site-packages" type="path"/>
  </client>
</tool>
EOF_TOOLFILE

export PYTHONV=$(echo $PYTHON_VERSION | cut -f1,2 -d.)

## IMPORT scram-tools-post
