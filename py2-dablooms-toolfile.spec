### RPM external py2-dablooms-toolfile 1.0
Requires: py2-dablooms
%prep

%build

%install

mkdir -p %{i}/etc/scram.d
cat << \EOF_TOOLFILE >%{i}/etc/scram.d/py2-dablooms.xml
<tool name="py2-dablooms" version="@TOOL_VERSION@">
  <info url="https://github.com/bitly/dablooms"/>
  <client>
    <environment name="PY2_DABLOOMS" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$PY2_DABLOOMS/lib"/>
    <runtime name="PYTHONPATH" value="$PY2_DABLOOMS/lib/python@PYTHONV@/site-packages" type="path"/>
  </client>
</tool>
EOF_TOOLFILE

export PYTHONV=$(echo $PYTHON_VERSION | cut -f1,2 -d.)

## IMPORT scram-tools-post
