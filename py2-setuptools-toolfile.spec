### RPM external py2-setuptools-toolfile 1.0
Requires: py2-setuptools
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/py2-setuptools.xml
<tool name="py2-setuptools" version="@TOOL_VERSION@">
  <client>
    <environment name="PY2_SETUPTOOLS_BASE" default="@TOOL_ROOT@"/>
  </client>
  <runtime name="PYTHONPATH" value="$PY2_SETUPTOOLS_BASE/lib/python@PYTHONV@/site-packages" type="path"/>
  <use name="python"/>
</tool>
EOF_TOOLFILE

export PYTHONV=$(echo $PYTHON_VERSION | cut -f1,2 -d.)

## IMPORT scram-tools-post

