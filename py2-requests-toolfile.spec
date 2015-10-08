### RPM external py2-requests-toolfile 1.0
Requires: py2-requests
%prep

%build

%install

mkdir -p %{i}/etc/scram.d
cat << \EOF_TOOLFILE >%{i}/etc/scram.d/py2-requests.xml
<tool name="py2-requests" version="@TOOL_VERSION@">
  <info url="http://docs.python-requests.org/en/latest/"/>
  <client>
    <environment name="PY2_REQUESTS" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$PY2_REQUESTS/lib"/>
    <runtime name="PYTHONPATH" value="$PY2_REQUESTS/lib/python@PYTHONV@/site-packages" type="path"/>
  </client>
</tool>
EOF_TOOLFILE

export PYTHONV=$(echo $PYTHON_VERSION | cut -f1,2 -d.)

## IMPORT scram-tools-post
