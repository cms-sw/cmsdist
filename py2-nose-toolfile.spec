### RPM external py2-nose-toolfile 1.0
Requires: py2-nose

%prep

%build

%install

mkdir -p %{i}/etc/scram.d
cat << \EOF_TOOLFILE >%{i}/etc/scram.d/py2-nose.xml
<tool name="py2-nose" version="@TOOL_VERSION@">
  <client>
    <environment name="PY2-NOSE_BASE" default="@TOOL_ROOT@"/>
  </client>
  <runtime name="PATH" value="$PY2-NOSE_BASE/bin" type="path"/>
</tool>
EOF_TOOLFILE


export PYTHON_LIB_SITE_PACKAGES
export PYTHON3_LIB_SITE_PACKAGES

## IMPORT scram-tools-post
