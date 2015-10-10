### RPM external py2-pysqlite-toolfile 1.0
Requires: py2-pysqlite
%prep

%build

%install

mkdir -p %{i}/etc/scram.d
cat << \EOF_TOOLFILE >%{i}/etc/scram.d/py2-pysqlite.xml
<tool name="py2-pysqlite" version="@TOOL_VERSION@">
  <info url="https://pypi.python.org/pypi/pysqlite"/>
  <client>
    <environment name="PY2_PYSQLITE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$PY2_PYSQLITE/lib"/>
    <runtime name="PYTHONPATH" value="$PY2_PYSQLITE/lib/python@PYTHONV@/site-packages" type="path"/>
  </client>
</tool>
EOF_TOOLFILE

export PYTHONV=$(echo $PYTHON_VERSION | cut -f1,2 -d.)

## IMPORT scram-tools-post
