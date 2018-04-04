### RPM external py2-lint-toolfile 1.0
Requires: py2-lint

%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/py2-lint.xml
<tool name="py2-lint" version="@TOOL_VERSION@">
  <client>
    <environment name="PY2_LINT_BASE" default="@TOOL_ROOT@"/>
  </client>
  <runtime name="PATH" value="$PY2_LINT_BASE/bin" type="path"/>
  <use name="python"/>
</tool>
EOF_TOOLFILE

export PYTHONV=$(echo $PYTHON_VERSION | cut -f1,2 -d.)

## IMPORT scram-tools-post
