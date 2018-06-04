### RPM external py2-numpy-toolfile 2.0
Requires: py2-numpy

%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/py2-numpy.xml
<tool name="py2-numpy" version="@TOOL_VERSION@">
  <client>
    <environment name="PY2_NUMPY_BASE" default="@TOOL_ROOT@"/>
  </client>
  <runtime name="PATH" value="$PY2_NUMPY_BASE/bin" type="path"/>
  <runtime name="PYTHON27PATH" value="$PY2_NUMPY_BASE/lib/python@PYTHONV@/site-packages/" type="path"/>
  <use name="python"/>
  <use name="zlib"/>
  <use name="lapack"/>
  <use name="OpenBLAS"/>
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
</tool>
EOF_TOOLFILE

export PYTHONV=$(echo $PYTHON_VERSION | cut -f1,2 -d.)
## IMPORT scram-tools-post
