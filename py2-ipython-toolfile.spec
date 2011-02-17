### RPM external py2-ipython-toolfile 1.0
Requires: py2-ipython
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/py2-ipython.xml
<tool name="py2-ipython" version="@TOOL_VERSION@">
  <client>
    <environment name="PY2_IPYTHON_BASE" default="@TOOL_ROOT@"/>
  </client>
  <runtime name="PATH" value="$PY2_IPYTHON_BASE/bin" type="path"/>
  <runtime name="PYTHONPATH" value="$PY2_IPYTHON_BASE/lib/python@PYTHONV@/site-packages" type="path"/>
  <use name="python"/>
</tool>
EOF_TOOLFILE

export PYTHONV=$(echo $PYTHON_VERSION | cut -f1,2 -d.)

## IMPORT scram-tools-post
