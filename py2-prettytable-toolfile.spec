### RPM external py2-prettytable-toolfile 1.0
Requires: py2-prettytable
%prep

%build

%install

mkdir -p %{i}/etc/scram.d
cat << \EOF_TOOLFILE >%{i}/etc/scram.d/py2-prettytable.xml
<tool name="py2-prettytable" version="@TOOL_VERSION@">
  <info url="https://code.google.com/p/prettytable"/>
  <client>
    <environment name="PY2_PRETTYTABLE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$PY2_PRETTYTABLE/lib"/>
    <runtime name="PYTHONPATH" value="$PY2_PRETTYTABLE/lib/python@PYTHONV@/site-packages" type="path"/>
  </client>
</tool>
EOF_TOOLFILE

export PYTHONV=$(echo $PYTHON_VERSION | cut -f1,2 -d.)

## IMPORT scram-tools-post
