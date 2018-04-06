### RPM external py2-nbformat-toolfile 1.0
Requires: py2-nbformat

%prep

%build

%install

mkdir -p %{i}/etc/scram.d
cat << \EOF_TOOLFILE >%{i}/etc/scram.d/py2-nbformat.xml
<tool name="py2-nbformat" version="@TOOL_VERSION@">
  <client>
    <environment name="PY2-NBFORMAT_BASE" default="@TOOL_ROOT@"/>
  </client>
  <runtime name="PATH" value="$PY2-NBFORMAT_BASE/bin" type="path"/>
</tool>
EOF_TOOLFILE


export PYTHON_LIB_SITE_PACKAGES
export PYTHON3_LIB_SITE_PACKAGES

## IMPORT scram-tools-post
