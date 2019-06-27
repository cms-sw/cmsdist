### RPM external py2-pybind11-toolfile 1.0
Requires: py2-pybind11

%prep

%build

%install

mkdir -p %{i}/etc/scram.d
cat << \EOF_TOOLFILE >%{i}/etc/scram.d/py2-pybind11.xml
<tool name="py2-pybind11" version="@TOOL_VERSION@">
  <client>
    <environment name="PY2_PYBIND11_BASE" default="@TOOL_ROOT@"/>
    <environment name="INCLUDE" default="$PY2_PYBIND11_BASE/include/python2.7"/>
  </client>
</tool>
EOF_TOOLFILE


export PYTHON_LIB_SITE_PACKAGES
export PYTHON3_LIB_SITE_PACKAGES

## IMPORT scram-tools-post
# bla bla
