### RPM external py2-PyYAML-toolfile 1.0
Requires: py2-PyYAML
%prep

%build

%install

mkdir -p %{i}/etc/scram.d
cat << \EOF_TOOLFILE >%{i}/etc/scram.d/py2-PyYAML.xml
<tool name="py2-PyYAML" version="@TOOL_VERSION@">
  <info url="https://github.com/PyYAML/PyYAML"/>
  <client>
    <environment name="PY2_PYYAML" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$PY2_PYYAML/lib"/>
    <runtime name="PYTHONPATH" value="$PY2_PYYAML/lib/python@PYTHONV@/site-packages" type="path"/>
  </client>
</tool>
EOF_TOOLFILE

export PYTHONV=$(echo $PYTHON_VERSION | cut -f1,2 -d.)

## IMPORT scram-tools-post
