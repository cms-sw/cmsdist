### RPM external py2-pip-toolfile 1.0
Requires: py2-pip
%prep

%build

%install

mkdir -p %{i}/etc/scram.d
cat << \EOF_TOOLFILE >%{i}/etc/scram.d/py2-pip.xml
<tool name="py2-pip" version="@TOOL_VERSION@">
  <info url="https://pypi.python.org/pypi/pip"/>
  <client>
    <environment name="PY2_PIP" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$PY2_PIP/lib"/>
    <runtime name="PYTHONPATH" value="$PY2_PIP/lib/python@PYTHONV@/site-packages" type="path"/>
    <runtime name="PATH" value="$PY2_PIP/bin" type="path"/>
  </client>
</tool>
EOF_TOOLFILE

export PYTHONV=$(echo $PYTHON_VERSION | cut -f1,2 -d.)

## IMPORT scram-tools-post
