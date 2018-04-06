### RPM external py2-jupyter_console-toolfile 1.0
Requires: py2-jupyter_console

%prep

%build

%install

mkdir -p %{i}/etc/scram.d
cat << \EOF_TOOLFILE >%{i}/etc/scram.d/py2-jupyter_console.xml
<tool name="py2-jupyter_console" version="@TOOL_VERSION@">
  <client>
    <environment name="PY2-JUPYTER_CONSOLE_BASE" default="@TOOL_ROOT@"/>
  </client>
  <runtime name="PATH" value="$PY2-JUPYTER_CONSOLE_BASE/bin" type="path"/>
</tool>
EOF_TOOLFILE


export PYTHON_LIB_SITE_PACKAGES
export PYTHON3_LIB_SITE_PACKAGES

## IMPORT scram-tools-post
