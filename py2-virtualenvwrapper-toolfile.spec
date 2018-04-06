### RPM external py2-virtualenvwrapper-toolfile 1.0
Requires: py2-virtualenvwrapper

%prep

%build

%install

mkdir -p %{i}/etc/scram.d
cat << \EOF_TOOLFILE >%{i}/etc/scram.d/py2-virtualenvwrapper.xml
<tool name="py2-virtualenvwrapper" version="@TOOL_VERSION@">
  <client>
    <environment name="PY2-VIRTUALENVWRAPPER_BASE" default="@TOOL_ROOT@"/>
  </client>
  <runtime name="PATH" value="$PY2-VIRTUALENVWRAPPER_BASE/bin" type="path"/>
</tool>
EOF_TOOLFILE


export PYTHON_LIB_SITE_PACKAGES
export PYTHON3_LIB_SITE_PACKAGES

## IMPORT scram-tools-post
