### RPM external py2-googlePackages-toolfile 1.0
Requires: py2-googlePackages

%prep

%build

%install

mkdir -p %{i}/etc/scram.d
cat << \EOF_TOOLFILE >%{i}/etc/scram.d/py2-googlePackages.xml
<tool name="py2-googlePackages" version="@TOOL_VERSION@">
  <client>
    <environment name="PY2_GOOGLEPACKAGES_BASE" default="@TOOL_ROOT@"/>
  </client>
  <runtime name="PATH" value="$PY2_GOOGLEPACKAGES_BASE/bin" type="path"/>
</tool>
EOF_TOOLFILE


export PYTHON_LIB_SITE_PACKAGES
export PYTHON3_LIB_SITE_PACKAGES

## IMPORT scram-tools-post
