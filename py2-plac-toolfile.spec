### RPM external py2-plac-toolfile 1.0
Requires: py2-plac

%prep

%build

%install

mkdir -p %{i}/etc/scram.d
cat << \EOF_TOOLFILE >%{i}/etc/scram.d/py2-plac.xml
<tool name="py2-plac" version="@TOOL_VERSION@">
  <client>
    <environment name="PY2-PLAC_BASE" default="@TOOL_ROOT@"/>
  </client>
  <runtime name="PATH" value="$PY2-PLAC_BASE/bin" type="path"/>
</tool>
EOF_TOOLFILE


export PYTHON_LIB_SITE_PACKAGES
export PYTHON3_LIB_SITE_PACKAGES

## IMPORT scram-tools-post
