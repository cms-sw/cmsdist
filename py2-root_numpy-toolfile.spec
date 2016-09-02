### RPM external py2-root_numpy-toolfile 1.0
Requires: py2-root_numpy
%prep

%build

%install

mkdir -p %{i}/etc/scram.d
cat << \EOF_TOOLFILE >%{i}/etc/scram.d/py2-root_numpy.xml
<tool name="py2-root_numpy" version="@TOOL_VERSION@">
  <info url="https://github.com/rootpy/root_numpy"/>
  <client>
    <environment name="PY2_ROOT_NUMPY" default="@TOOL_ROOT@"/>
    <runtime name="PYTHONPATH" value="$PY2_ROOT_NUMPY/lib/python@PYTHONV@/site-packages" type="path"/>
  </client>
</tool>
EOF_TOOLFILE

export PYTHONV=$(echo $PYTHON_VERSION | cut -f1,2 -d.)

## IMPORT scram-tools-post
