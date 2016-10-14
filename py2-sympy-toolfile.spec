### RPM external py2-sympy-toolfile 1.0
Requires: py2-sympy
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/py2-sympy.xml
<tool name="py2-sympy" version="@TOOL_VERSION@">
  <client>
    <environment name="PY2SYMPY_BASE" default="@TOOL_ROOT@"/>
  </client>
  <runtime name="PYTHONPATH" value="$PY2SYMPY_BASE/lib/python@PYTHONV@/site-packages" type="path"/>
  <use name="python"/>
</tool>
EOF_TOOLFILE

export PYTHONV=$(echo $PYTHON_VERSION | cut -f1,2 -d.)

## IMPORT scram-tools-post
