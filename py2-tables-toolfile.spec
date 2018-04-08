### RPM external py2-tables-toolfile 1.0
Requires: py2-tables

%prep

%build

%install

mkdir -p %{i}/etc/scram.d
cat << \EOF_TOOLFILE >%{i}/etc/scram.d/py2-tables.xml
<tool name="py2-tables" version="@TOOL_VERSION@">
  <client>
    <environment name="PY2-TABLES_BASE" default="@TOOL_ROOT@"/>
  </client>
  <runtime name="PATH" value="$PY2-TABLES_BASE/bin" type="path"/>
</tool>
EOF_TOOLFILE


export PYTHON_LIB_SITE_PACKAGES
export PYTHON3_LIB_SITE_PACKAGES

## IMPORT scram-tools-post
