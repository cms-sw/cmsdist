### RPM external py2-futures-toolfile 1.0
Requires: py2-futures
%prep

%build

%install

mkdir -p %{i}/etc/scram.d
cat << \EOF_TOOLFILE >%{i}/etc/scram.d/py2-futures.xml
<tool name="py2-futures" version="@TOOL_VERSION@">
  <info url="https://pypi.python.org/pypi/MarkupSafe"/>
  <client>
    <environment name="PY2_FUTURES" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$PY2_FUTURES/lib"/>
    <runtime name="PYTHONPATH" value="$PY2_FUTURES/lib/python@PYTHONV@/site-packages" type="path"/>
  </client>
</tool>
EOF_TOOLFILE

export PYTHONV=$(echo $PYTHON_VERSION | cut -f1,2 -d.)

## IMPORT scram-tools-post
