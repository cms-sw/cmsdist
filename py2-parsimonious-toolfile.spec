### RPM external py2-parsimonious-toolfile 1.0
Requires: py2-parsimonious
%prep

%build

%install

mkdir -p %{i}/etc/scram.d
cat << \EOF_TOOLFILE >%{i}/etc/scram.d/py2-parsimonious.xml
<tool name="py2-parsimonious" version="@TOOL_VERSION@">
  <info url="https://pypi.python.org/pypi/MarkupSafe"/>
  <client>
    <environment name="PY2_PARSIMONIOUS_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$PY2_PARSIMONIOUS_BASE/lib"/>
    <runtime name="PYTHONPATH" value="$PY2_PARSIMONIOUS_BASE/lib/python@PYTHONV@/site-packages" type="path"/>
  </client>
</tool>
EOF_TOOLFILE

export PYTHONV=$(echo $PYTHON_VERSION | cut -f1,2 -d.)

## IMPORT scram-tools-post
