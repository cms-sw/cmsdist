### RPM external py2-numpy-toolfile 1.0
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
  <runtime name="PYTHONPATH" value="$PY2_NUMPY_BASE/lib/python@PYTHONV@/site-packages" type="path"/>
  <use name="python"/>
  <use name="zlib"/>
  <use name="lapack"/>
  <use name="OpenBLAS"/>
</tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%{i}/etc/scram.d/py2-numpy-c-api.xml
<tool name="py2-numpy-c-api" version="@TOOL_VERSION@">
  <client>
    <environment name="PY2_NUMPY_C_API_BASE" default="@TOOL_ROOT@"/>
    <environment name="INCLUDE" default="$PY2_NUMPY_C_API_BASE/c-api/core/include"/>
  </client>
  <use name="python"/>
</tool>
EOF_TOOLFILE

export PYTHONV=$(echo $PYTHON_VERSION | cut -f1,2 -d.)
## IMPORT scram-tools-post
