### RPM external py2-python-dateutil-toolfile 1.0
Requires: py2-python-dateutil
%prep

%build

%install

mkdir -p %{i}/etc/scram.d
cat << \EOF_TOOLFILE >%{i}/etc/scram.d/py2-python-dateutil.xml
<tool name="py2-python-dateutil" version="@TOOL_VERSION@">
  <client>
    <environment name="PY2_PYTHON_DATEUTIL_BASE" default="@TOOL_ROOT@"/>
  </client>
  <runtime name="PYTHONPATH" value="$PY2_PYTHON_DATEUTIL_BASE/lib/python@PYTHONV@/site-packages" type="path"/>
  <use name="python"/>
</tool>
EOF_TOOLFILE

export PYTHONV=$(echo $PYTHON_VERSION | cut -f1,2 -d.)
## IMPORT scram-tools-post
