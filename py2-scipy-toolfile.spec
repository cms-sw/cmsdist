### RPM external py2-scipy-toolfile 1.0
Requires: py2-scipy
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/py2-scipy.xml
<tool name="py2-scipy" version="@TOOL_VERSION@">
  <client>
    <environment name="PY2SHIPY_BASE" default="@TOOL_ROOT@"/>
  </client>
  <runtime name="PYTHONPATH" value="$PY2SHIPY_BASE/lib/python@PYTHONV@/site-packages" type="path"/>
  <use name="python"/>
  <use name="py2-numpy"/>
  <use name="lapack"/>
</tool>
EOF_TOOLFILE

export PYTHONV=$(echo $PYTHON_VERSION | cut -f1,2 -d.)

## IMPORT scram-tools-post
