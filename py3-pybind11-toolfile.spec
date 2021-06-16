### RPM external py3-pybind11-toolfile 1.0
Requires: py3-pybind11

%prep

%build

%install

mkdir -p %{i}/etc/scram.d
cat << \EOF_TOOLFILE >%{i}/etc/scram.d/py3-pybind11.xml
<tool name="py3-pybind11" version="@TOOL_VERSION@">
  <client>
    <environment name="PY3_PYBIND11_BASE" default="@TOOL_ROOT@"/>
    <environment name="INCLUDE" default="$PY3_PYBIND11_BASE/lib/python3.8/site-packages/pybind11/include"/>
  </client>
</tool>
EOF_TOOLFILE

export PYTHON3_LIB_SITE_PACKAGES

## IMPORT scram-tools-post
