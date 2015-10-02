### RPM external py2-six-toolfile 1.0
Requires: py2-six
%prep

%build

%install

mkdir -p %{i}/etc/scram.d
cat << \EOF_TOOLFILE >%{i}/etc/scram.d/py2-six.xml
<tool name="py2-six" version="@TOOL_VERSION@">
  <info url="https://pypi.python.org/pypi/six"/>
  <client>
    <environment name="PY2_SIX" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$PY2_SIX/lib"/>
    <runtime name="PYTHONPATH" value="$PY2_SIX/lib/python@PYTHONV@/site-packages" type="path"/>
  </client>
</tool>
EOF_TOOLFILE

export PYTHONV=$(echo $PYTHON_VERSION | cut -f1,2 -d.)

## IMPORT scram-tools-post
