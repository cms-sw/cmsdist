### RPM external py3-numpy-toolfile 1.0
Requires: py3-numpy

%prep

%build

%install

mkdir -p %{i}/etc/scram.d
cat << \EOF_TOOLFILE >%{i}/etc/scram.d/py3-numpy.xml
<tool name="py3-numpy" version="@TOOL_VERSION@">
  <client>
    <environment name="PY3_NUMPY_BASE" default="@TOOL_ROOT@"/>
  </client>
  <runtime name="PATH" value="$PY3_NUMPY_BASE/bin" type="path"/>
</tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%{i}/etc/scram.d/numpy-c-api.xml
<tool name="numpy-c-api" version="@TOOL_VERSION@">
  <lib name="npymath"/>
  <client>
    <environment name="NUMPY_C_API_BASE" default="@TOOL_ROOT@"/>
    <environment name="INCLUDE" default="$NUMPY_C_API_BASE/c-api/core/include"/>
    <environment name="LIBDIR" default="$NUMPY_C_API_BASE/c-api/core/lib"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
