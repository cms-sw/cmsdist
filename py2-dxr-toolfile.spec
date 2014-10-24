### RPM external py2-dxr-toolfile 1.0
Requires: py2-dxr py2-futures py2-jinja py2-markupsafe py2-ordereddict py2-parsimonious
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
    <runtime name="PYTHONPATH" value="$PY2_DXR_BASE/lib/python@PYTHONV@/site-packages" type="path"/>
    <runtime name="PATH" value="$PY2_DXR_BASE/bin" type="path"/>
    <use name="python"/>
    <use name="sqlite"/>
    <use name="py2-futures"/>
    <use name="py2-jinja"/>
    <use name="py2-markupsafe"/>
    <use name="py2-ordereddict"/>
    <use name="py2-parsimonious"/>
    <use name="py2-pygments"/>
</tool>
EOF_TOOLFILE

export PYTHONV=$(echo $PYTHON_VERSION | cut -f1,2 -d.)

## IMPORT scram-tools-post
