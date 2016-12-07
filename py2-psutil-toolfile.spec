### RPM external py2-psutil-toolfile 1.0
Requires: py2-psutil
%prep

%build

%install

mkdir -p %{i}/etc/scram.d
cat << \EOF_TOOLFILE >%{i}/etc/scram.d/py2-psutil.xml
<tool name="py2-psutil" version="@TOOL_VERSION@">
  <info url="https://github.com/giampaolo/psutil"/>
  <client>
    <environment name="PY2_PSUTIL" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$PY2_PSUTIL/lib"/>
    <runtime name="PYTHONPATH" value="$PY2_PSUTIL/lib/python@PYTHONV@/site-packages" type="path"/>
  </client>
</tool>
EOF_TOOLFILE

export PYTHONV=$(echo $PYTHON_VERSION | cut -f1,2 -d.)

## IMPORT scram-tools-post
