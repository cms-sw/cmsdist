### RPM external py2-dxr-toolfile 1.0
Requires: py2-dxr  py2-pippkgs py2-pysqlite
%prep

%build

%install

mkdir -p %{i}/etc/scram.d
cat << \EOF_TOOLFILE >%{i}/etc/scram.d/py2-dxr.xml
<tool name="py2-dxr" version="@TOOL_VERSION@">
  <info url="https://dxr.readthedocs.org/"/>
  <client>
    <environment name="PY2_DXR_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$PY2_DXR_BASE/lib"/>
  </client>
    <runtime name="PATH" value="$PY2_DXR_BASE/bin" type="path"/>
    <use name="python"/>
    <use name="sqlite"/>
    <use name="py2-pysqlite"/>
    <use name="py2-pippkgs"/>
</tool>
EOF_TOOLFILE

export PYTHONV=$(echo $PYTHON_VERSION | cut -f1,2 -d.)

## IMPORT scram-tools-post
