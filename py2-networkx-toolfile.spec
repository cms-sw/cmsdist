### RPM external py2-networkx-toolfile 1.0
Requires: py2-networkx
%prep

%build

%install

mkdir -p %{i}/etc/scram.d
cat << \EOF_TOOLFILE >%{i}/etc/scram.d/py2-networkx.xml
<tool name="py2-networkx" version="@TOOL_VERSION@">
  <info url="https://pypi.python.org/pypi/networkx"/>
  <client>
    <environment name="PY2_NETWORKX" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$PY2_NETWORKX/lib"/>
    <runtime name="PYTHONPATH" value="$PY2_NETWORKX/lib/python@PYTHONV@/site-packages" type="path"/>
  </client>
</tool>
EOF_TOOLFILE

export PYTHONV=$(echo $PYTHON_VERSION | cut -f1,2 -d.)

## IMPORT scram-tools-post
