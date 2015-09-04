### RPM external py2-schema-toolfile 1.0
Requires: py2-schema
%prep

%build

%install

mkdir -p %{i}/etc/scram.d
cat << \EOF_TOOLFILE >%{i}/etc/scram.d/py2-schema.xml
<tool name="py2-schema" version="@TOOL_VERSION@">
  <info url="https://pypi.python.org/pypi/schema"/>
  <client>
    <environment name="PY2_SCHEMA" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$PY2_SCHEMA/lib"/>
    <runtime name="PYTHONPATH" value="$PY2_SCHEMA/lib/python@PYTHONV@/site-packages" type="path"/>
  </client>
</tool>
EOF_TOOLFILE

export PYTHONV=$(echo $PYTHON_VERSION | cut -f1,2 -d.)

## IMPORT scram-tools-post
