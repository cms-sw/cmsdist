### RPM external py2-python_tools-toolfile 1.0
Requires: python_tools

%prep

%build

%install

# we need to include any executable paths that we want here (and corresponding
# LD_LIBRARY_PATHs

mkdir -p %{i}/etc/scram.d
cat << \EOF_TOOLFILE >%{i}/etc/scram.d/py2-python_tools.xml
<tool name="py2-pip" version="@TOOL_VERSION@">
  <info url="https://pypi.python.org/pypi/pip"/>
  <client>
    <environment name="PYTHON_TOOLS" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$PY2_PIP_BASE/lib"/>
    <runtime name="PATH" value="$PY2_PIP_BASE/bin" type="path"/>
  </client>
</tool>
EOF_TOOLFILE

export PYTHONV=$(echo $PYTHON_VERSION | cut -f1,2 -d.)

## IMPORT scram-tools-post
