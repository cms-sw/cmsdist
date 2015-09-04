### RPM external py2-pandas-toolfile 1.0
Requires: py2-pandas
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/py2-pandas.xml
<tool name="py2-pandas" version="@TOOL_VERSION@">
  <client>
    <environment name="PY2_PANDAS_BASE" default="@TOOL_ROOT@"/>
  </client>
  <runtime name="PYTHONPATH" value="$PY2_PANDAS_BASE/lib/python@PYTHONV@/site-packages" type="path"/>
  <use name="python"/>
  <use name="py2-numpy"/>
  <use name="py2-python-dateutil"/>
  <use name="py2-pytz"/>
</tool>
EOF_TOOLFILE

export PYTHONV=$(echo $PYTHON_VERSION | cut -f1,2 -d.)

## IMPORT scram-tools-post
