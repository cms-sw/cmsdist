### RPM external py2-fs-toolfile 1.0
Requires: py2-fs

%prep

%build

%install

mkdir -p %{i}/etc/scram.d
cat << \EOF_TOOLFILE >%{i}/etc/scram.d/py2-fs.xml
<tool name="py2-fs" version="@TOOL_VERSION@">
  <client>
    <environment name="PY2_FS_BASE" default="@TOOL_ROOT@"/>
  </client>
</tool>
EOF_TOOLFILE


export PYTHON_LIB_SITE_PACKAGES
export PYTHON3_LIB_SITE_PACKAGES

## IMPORT scram-tools-post
