### RPM external py2-rootpy-toolfile 1.0
Requires: py2-rootpy
%prep

%build

%install

mkdir -p %{i}/etc/scram.d
cat << \EOF_TOOLFILE >%{i}/etc/scram.d/py2-root_numpy.xml
<tool name="py2-rootpy" version="@TOOL_VERSION@">
  <info url="https://github.com/rootpy/rootpy"/>
  <client>
    <environment name="PY2_ROOTPY" default="@TOOL_ROOT@"/>
    <runtime name="PYTHONPATH" value="$PY2_ROOTPY/lib/python@PYTHONV@/site-packages" type="path"/>
  </client>
</tool>
EOF_TOOLFILE

export PYTHONV=$(echo $PYTHON_VERSION | cut -f1,2 -d.)

## IMPORT scram-tools-post
