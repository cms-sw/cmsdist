### RPM external py3-dxr-toolfile 1.0
Requires: py3-dxr

%prep

%build

%install

mkdir -p %{i}/etc/scram.d
cat << \EOF_TOOLFILE >%{i}/etc/scram.d/py2-dxr.xml
<tool name="py2-dxr" version="@TOOL_VERSION@">
  <client>
    <environment name="PY2_DXR_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$PY2_DXR_BASE/lib"/>
  </client>
  <runtime name="PATH" value="$PY2_DXR_BASE/bin" type="path"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
