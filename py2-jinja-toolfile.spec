### RPM external py2-jinja-toolfile 1.0
Requires: py2-jinja
%prep

%build

%install

mkdir -p %{i}/etc/scram.d
cat << \EOF_TOOLFILE >%{i}/etc/scram.d/py2-jinja.xml
<tool name="py2-jinja" version="@TOOL_VERSION@">
  <info url="https://pypi.python.org/pypi/jinja"/>
  <client>
    <environment name="PY2_JINJA_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$PY2_JINJA_BASE/lib"/>
    <runtime name="PYTHONPATH" value="$PY2_JINJA_BASE/lib/python@PYTHONV@/site-packages" type="path"/>
  </client>
</tool>
EOF_TOOLFILE

export PYTHONV=$(echo $PYTHON_VERSION | cut -f1,2 -d.)

## IMPORT scram-tools-post
