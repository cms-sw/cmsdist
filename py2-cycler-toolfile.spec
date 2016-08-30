### RPM external py2-cycler-toolfile 1.0
Requires: py2-cycler
%prep

%build

%install

mkdir -p %{i}/etc/scram.d
cat << \EOF_TOOLFILE >%{i}/etc/scram.d/py2-cycler.xml
<tool name="py2-cycler" version="@TOOL_VERSION@">
  <info url="https://github.com/matplotlib/cycler"/>
  <client>
    <environment name="PY2_CYCLER" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$PY2_CYCLER/lib"/>
    <runtime name="PYTHONPATH" value="$PY2_CYCLER/lib/python@PYTHONV@/site-packages" type="path"/>
  </client>
</tool>
EOF_TOOLFILE

export PYTHONV=$(echo $PYTHON_VERSION | cut -f1,2 -d.)

## IMPORT scram-tools-post
